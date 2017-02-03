import urllib2
import numpy as np
import os
import re
import time
import random

folders = os.listdir("./downloads")

def get_urls(filename):
	"""Takes in a filename and returns all the urls in that file"""
	urls = None
	if os.path.isfile(filename):
		file_str = open(filename,"r").read()
		urls = re.findall("http://([A-Za-z0-9-'*]{0,15}.livejournal.com/[0-9]{1,4}.html)", file_str)
	return urls

def extract_username(url):
	"""Takes in a url and returns the usernames in the source code"""
	response = urllib2.urlopen(url)
	page_source = response.read()
	results = re.findall('"username":"[A-Za-z_0-9*]{1,20}"', page_source)
	processed = []
	for s in results:
		processed.append(s[12:-1])
	if len(processed)>0:
		return set(processed)
	else:
		return None

urls = [] 

for f in folders:
	print(f)
	try:
		for fi in os.listdir("./downloads/"+f):
			new_urls = get_urls("./downloads/"+f+"/"+fi)
			if new_urls is not None:
				urls.extend(new_urls)
	except OSError:
		pass

thefile = open('new_usernames.txt', 'a')
new_usernames = []
print(len(urls))
for u in urls:
	try:	
		usernames = extract_username("http://"+u)
	except urllib2.HTTPError:
		usernames=None
		time.sleep(60)
		pass
	time.sleep(1+random.random())
	if usernames is not None:
		for item in list(usernames):
			if item not in new_usernames:
				print("Added new username")
				new_usernames.append(item)
				thefile.write("%s\n" % item)
