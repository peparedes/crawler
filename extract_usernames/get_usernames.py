# -*- coding: utf-8 -*-
#Python 2 script
import urllib2
import re
import os

def extract_username(url):
	"""Takes in a url and returns the useranames in the source code"""
	response = urllib2.urlopen(url)
	page_source = response.read()
	results = re.findall('"username":"[A-Za-z_0-9*]{1,20}"', page_source)
	processed = []
	for s in results:
		processed.append(s[12:-1])
	if len(processed)>0:
		return processed[0]
	else:
		return None

#get all files from directory
files = os.listdir("../downloads")
searched_files = [] # this is another file that keeps track of the explored files
with open('searched_files.txt', 'r') as sf:
	searched_files.extend(sf.read().splitlines()) #import all the already explored files

tmp = []
with open('new_usernames.txt', 'r') as sf:
	tmp.extend(sf.read().splitlines()) #import all the already explored files
print(tmp)
#set that keeps usernames so that they are not repeated in the file
usernames = set(tmp)
print(usernames)

#extract urls from all the files
for n in range(len(files)):
	# every 5 files you look at save the usernames to the new_usernames  file
	if not n%5:
		new_file = open('new_usernames.txt', 'w')
		sf = open('searched_files.txt', 'a')
		for item in usernames:
  			print>>new_file, item

	f = files[n]
	print(str(n)+" of "+str(len(files))+" files.")
	#file should exist in the downloads folder and should not have been searched yet
	if os.path.isfile("../downloads/"+f) and f not in searched_files:
		print>>sf, f
		file_str = open("../downloads/"+f,"r").read()
		try:
			urls = re.findall("http://([A-Za-z0-9-'*]{0,15}.livejournal.com/[0-9]{1,4}.html)", file_str)
			if len(urls)>0:
				for url in urls:
					u = extract_username("http://"+url)
					usernames.add(u)
		except AttributeError:
			pass
print usernames 






