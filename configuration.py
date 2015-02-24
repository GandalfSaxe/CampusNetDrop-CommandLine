import os
import CampusNetDrop as cnd
import xml.etree.ElementTree as ET

dirname, filename = os.path.split(os.path.abspath(__file__))

### login
if not os.path.isfile(dirname+"/lmtdAccss.txt"):
	cnd.login()
else:
	print("Configure login? (yes/no)")
	configure = input()
	if configure == "yes" or configure == "y":
		cnd.login()

### Config
print("Configure courses? (yes/no)")
configure = input()
if configure == "yes" or configure == "y":
	# Create request and load XML into 'root'
	url = 'https://www.campusnet.dtu.dk/data/CurrentUser/Elements'
	response = cnd.sendRequest(url)
	root = ET.fromstring(response.text)
	# Run through 'root' node and save elementID, download path and versioning in config
	f = open(dirname+'/config.txt','w')
	for node in root:
		for child in node:
			print("Add \"%s --- %s\" to Downloads? (y/n)" % (node.get('Name'),child.get('Name')))
			answer = input()

			if answer=="yes" or answer=="y":
				print("Where to download the \"%s\" files? (Path)" % (child.get('Name')))
				directory = input()
				directory = directory.replace("\\","/")
				f.write(child.get('Name')+";"+child.get('Id')+";"+directory+"\n")
	f.close()
