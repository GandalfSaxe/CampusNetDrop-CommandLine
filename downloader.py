import datetime, os
import CampusNetDrop as cnd
import xml.etree.ElementTree as ET


dirname, filename = os.path.split(os.path.abspath(__file__))

### Downloader
# Load Config
with open(dirname+'/config.txt') as f:
	lines = f.readlines()

# Run through courses
for line in lines:
	line = line.strip()
	line = line.split(";")
	elementID = line[1]
	directory = line[2]
	print("\n### ",end='')
	print(line[0],end='')
	print(" ### ")

	# get files of course from xml
	url='https://www.campusnet.dtu.dk/data/CurrentUser/Elements/%s/Files' % (str(elementID))
	response = cnd.sendRequest(url)
	root = ET.fromstring(response.text)

	# create folder structure
	cnd.createFolders(root,directory)
	to_download = []
	# get files to download
	cnd.getFiles(root,"",to_download)
	for download in to_download:
		# download file if it doesnt exist or if there is a new version
		file_path = directory+download['Path']+"/"+download['Name']
		if os.path.isfile(file_path):
			file_created = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
			if not file_created > download['Created']:
				cnd.download_file(elementID,download['Id'],file_path)
			# else:
				# print("Latest version already downloaded. "+download['Path']+"/"+download['Name'])
		else:
			cnd.download_file(elementID,download['Id'],file_path)