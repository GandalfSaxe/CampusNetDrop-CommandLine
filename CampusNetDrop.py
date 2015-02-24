import os, datetime, getpass, requests
import xml.etree.ElementTree as ET

def sendRequest(url):
	dirname, filename = os.path.split(os.path.abspath(__file__))
	with open(dirname+"/token.txt") as f:
		data = f.readlines()
	appName = data[0].strip()
	appToken = data[1].strip()
	with open(dirname+"/lmtdAccss.txt") as f:
		lines = f.readlines()
	PApassword = lines[0].strip()
	username = lines[1].strip()
	headers = {'X-appname' : appName, 'X-token' : appToken}
	return requests.get(url,auth=(username,PApassword),headers=headers)

def createFolders(root,path):
	"""Run through XML nodes and copy folder structure into 'path' """
	for node in root:
		if node.tag == "Folder":
			createFolder(node.get('Name'),path)
			if len(node):
				createFolders(node,path+"/"+node.get('Name'))

def createFolder(name,path):
	"""Create folder if not already there"""
	directory = path+"/"+name
	if not os.path.isdir(directory):
		print("Creating folder "+path+"/"+name)
		os.makedirs(directory)

def getFiles(root,path,to_download):
	"""Fill list of all files you could possible download"""
	for node in root:
		if node.tag == "File":
			#print("Files found "+path+"/"+node.get('Name'))
			created = getLatestVersion(node)
			to_download.append({'Id':node.get('Id'), 'Name':node.get('Name'),'Path':path,'Created':created})
		if len(node):
			getFiles(node,path+"/"+node.get('Name'),to_download)

def getLatestVersion(root):
	"""Check all versions for latest date"""
	first_run = True
	for node in root.iter('FileVersion'):
		if first_run:
			latest_date = datetime.datetime.strptime(node.get('Created').split(".")[0], "%Y-%m-%dT%H:%M:%S")
		else:
			new_date = datetime.datetime.strptime(node.get('Created').split(".")[0], "%Y-%m-%dT%H:%M:%S")
			if new_date > latest_date:
				latest_date = new_date
		first_run = False
	return latest_date

def download_file(elementID,downloadID,file_path):
	"""Simply download a file"""
	print("Downloading file "+file_path)
	url='https://www.campusnet.dtu.dk/data/CurrentUser/Elements/%s/Files/%s/Bytes' % (str(elementID),str(downloadID))
	response = sendRequest(url)
	data = response.content
	with open(file_path, 'wb') as f:
		f.write(data)

def login():
	"""Login during configuration"""
	"""Gets a protected access password from CN """
	print("CampusNet username? (sXXXXXX)")
	username = input().strip()
	print("CampusNet password?")
	pwd = getpass.getpass().strip()
	url = 'https://auth.dtu.dk/dtu/mobilapp.jsp'
	values = {'username' : username, 'password' : pwd}
	response = requests.post(url, data=values)
	xml_root = ET.fromstring(response.text)
	PApassword = xml_root.find('LimitedAccess').get('Password')
	dirname, filename = os.path.split(os.path.abspath(__file__))
	f = open(dirname+'/lmtdAccss.txt','w')
	f.write(str(PApassword) + "\n" + str(username))
	f.close()
