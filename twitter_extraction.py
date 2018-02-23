import json
import re
import os
import fnmatch

def updateJsonFile(flag, fileName):	
	with open('/Users/victor/Desktop/DSlab/Twitter2/'+fileName, 'r', encoding='utf-8') as jsonFile:
		data = json.load(jsonFile) #Open file and dump contents into "data"

	urlPattern = re.compile(r"(http:|https:|ftp:|ftps:)(\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?)")
	# WORK on "data", making a changes to the JSON file as needed	
	
	if flag != None: # (IF MATCH) Search for "label:(0|1)""\ in each line 
		if flag[0] == '1':
			data['rumor_label'] = True
		elif flag[0] == '0':
			data['rumor_label'] = False
	for each in data['TweetsList']: 
			detailsContent = each['detail']
			urlsFound = urlPattern.search(detailsContent) #Matching urls
			if urlsFound != None:
				each['containURL'] = True
			else:
				each['containURL'] = False

	for each in data['TweetsList']:
		detailsContent = each['detail']
		verificationPattern = re.search('('+')|('.join([ 'is (that|this|it) true', '( real? | really ? | unconfirmed )', '(rumor | debunk)', '(that|this|it) is not true', 'wh[a]*t[?!][?1]*'])+')', detailsContent)
		if verificationPattern != None: #If regEx match
			data['isConflicted'] = True
			verifyList = verificationPattern.group()
			correction = re.search('('+')|('.join([ '(rumor | debunk)', '(that|this|it) is not true'])+')', verifyList)
			verification = re.search('('+')|('.join([ 'is (that|this|it) true', '( real? | really ? | unconfirmed )', 'wh[a]*t[?!][?1]*'])+')', verifyList)
			if correction != None: #Correction found update data['hasCorrection'] to True
				each['hasCorrection'] = True
			elif correction == None:
				each['hasCorrection'] = False
			if verification != None:
				each['hasVerification'] = True
			elif verification == None:
				each['hasVerification'] = False
	
	#Open and dump updated JSON file
	with open('/Users/victor/Desktop/DSlab/Twitter2/'+fileName, 'w', encoding='utf-8') as jsonFile: 
		json.dump(data, jsonFile, indent=2) #Reopen Json file this time to write the new value

def searchForJsonFile(flag, eidName):

	for files in os.listdir('/Users/victor/Desktop/DSlab/Twitter2'):
		fileName = 'rumor_'+eidName+'.json'
		if fnmatch.fnmatch(files, fileName):
			updateJsonFile(flag, fileName)

lines = [] #List where each event in twitter.txt will live 
labelPattern = re.compile(r"label:(0|1)") #RegularEx to search for "Label: 0 | 1"
idPattern = re.compile(r"(?m)(?<=\beid:)\S{3,}") #regEx for .json name 

#Open and read Twitter.txt extract the label to verify if tweet is a rumor (1) or otherwise (0)
with open("Twitter.txt", "rt") as twitterFile:
	for lines in twitterFile: # Store each line in twitterFile into variable "line"
		contents = labelPattern.findall(lines) #"Contents" holds 1 or 0 flaging wether tweet is a rumor or not
		eid = idPattern.findall(lines) #"eid" holds the name of each .json file 
		searchForJsonFile(contents[0], eid[0])
		

				
	
