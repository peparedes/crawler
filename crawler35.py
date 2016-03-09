import time
import sys
from os import popen
import subprocess
import shlex
from lxml import etree
import os
from time import sleep
import base64

# crawler account
username = 'bidbt'#'kenghao'#
password = 'bid35460'#'smallcat1003'#


def crawl ():
	# read name-id file
	f = open(r'../data/name2id', 'r')
	nameid = map(lambda line: line.rstrip('\n').split('|').pop(1), f.readlines())
	nameid = map(lambda line: line.rstrip('\n').split('|').pop(1), f.readlines())
	i = 0
	while True:
		time.sleep(0.2)
		print(nameid[i])
		i = i + 1


def ljquery_flat ():
	curl = 'curl -d mode=login -d user=bidbt -d password=bid35460 http://www.livejournal.com/interface/flat'
	pp = subprocess.Popen(shlex.split(curl),stdout=subprocess.PIPE)
	print(pp.stdout.read())

def ljquery_xmlrpc ():
	xml = startXMLStr();
	xml = appendModule(xml, 'LJ.XMLRPC.login');
	xml = appendParamMember(xml, 'username', 'bidbt', 'string');
	xml = appendParamMember(xml, 'password', 'bid35460', 'string');
	xml = endXmlStr(xml);

	curl = 'curl -d "'+xml+'" http://www.livejournal.com/interface/xmlrpc'
	#print(curl
	pp = subprocess.Popen(shlex.split(curl),stdout=subprocess.PIPE)
#	print(pp.stdout.read()
	content = pp.stdout.read()
	f = open('out.xml', 'w')
	f.write(content)
#	print(content

def unflat(xmldoc,f, elementname, tag, tagval, isroot, rettag):
	child = xmldoc
	#print(>>f, child

	retval = ""
	count = 0;
	while child is not None:

		pairs = child.children.children
		if isroot:
			print("<%s>" % (elementname), file=f)
			#f.write("<%s>" % (elementname))
			print("<%s>%s</%s>" % (tag, tagval, tag), file=f)
			#f.write("<%s>" % (elementname))
			count = count + 1

		while pairs is not None:
			#print >>f, pairs
			values = pairs.children

			name = values.content
			val = values.next.children.content
			if name != "props":
				#print(>>f, "<%s><![CDATA[%s]]></%s>" % (name, val, name)

				print("<%s>%s</%s>" % (name, values.next.children, name), file=f)

				#if name == "event" or name == "subject" or name == "current_mood":
				#	print(>>f, "<%s><![CDATA[%s]]></%s>" % (name, val, name)
				#else:
				#	print(>>f, "<%s>%s</%s>" % (name, val, name)
			else:
				print("<props>", file=f)
 				#print(>>f, values.next
				unflat(values.next, f, elementname, tag, tagval, 0, "")
				print("</props>", file=f)

			if isroot and name == rettag:
				retval = val


			pairs = pairs.next
		if isroot:
			print("</%s>" % (elementname), file=f)

 		#print(child
 		#print(>>f, child
		child = child.next

	if isroot:
		print("count:%d" % (count))
	return retval



def genNewXmlForElement(f, xml, element, tag, tagval, rettag):
	doc = etree.parse(xml)#libxml2.parseDoc(xml)
	root = doc.root[0] #root = doc.children.children.children.children.children

	#print(root
	child = root.children
	while child is not None:
		if child.children.content != element:
	#		child = child.next
			node = child
			node.unlinkNode()
			node.freeNode()
		#else:
			#node = new_node("uid")
			#node.content = "test"
			#child.addChild(node)


		child = child.next
	#print(root

	#print(>>f, root

	# unflat jason like xml: root

	print("<posts>", file=f)
	child = root.children.children
	child = child.next
	try:
		child = child.children.children.children
		retval = unflat(child, f, "post", tag, tagval, 1, rettag)
	except:
		retval = ""

	print("</posts>", file=f)

	return retval

def startXMLStr():
	return '<?xml version=\\"1.0\\"?><methodCall>'

def appendModule(xml, modName):
	return xml+'<methodName>'+modName+'</methodName><params><param><value><struct>'

def endXmlStr(xml):
	return xml + '<member><name>ver</name><value><int>1</int></value></member></struct></value></param></params></methodCall>'

def appendParamMember(xml, name, val, valtype):
	return xml+'<member><name>'+name+'</name><value><'+valtype+'>'+val+'</'+valtype+'></value></member>'

#
def lj_getevents(target_user, index, beforedate):
	xml = startXMLStr();
	xml = appendModule(xml, 'LJ.XMLRPC.getevents');
	xml = appendParamMember(xml, 'username', username, 'string');
	xml = appendParamMember(xml, 'password', password, 'string');
	xml = appendParamMember(xml, 'selecttype', 'lastn', 'string');
	xml = appendParamMember(xml, 'howmany', '50', 'int');
	xml = appendParamMember(xml, 'usejournal', target_user, 'string');
	if beforedate != "":
		xml = appendParamMember(xml, 'beforedate', beforedate, 'string');
	xml = endXmlStr(xml);

	curl = 'curl -d "'+xml+'" http://www.livejournal.com/interface/xmlrpc'
	#print(curl
	pp = subprocess.Popen(shlex.split(curl),stdout=subprocess.PIPE)
	# may cause deadlock
	#content = pp.stdout.read()
	content = pp.communicate()[0]
	f = open('response.xml', 'w')
	print(content)
	f.write(content.decode("utf-8"))
	f.close()
	#print(content
	f = open("../data/events/%010d/%s_%010d.xml" % (index,target_user,index), 'w+')
	retval = genNewXmlForElement(f, content, "events", "user", target_user, "eventtime")
	f.close()
#	while pp.poll() == None:
#		pp.terminate()
#	pp.wait() # wait for it to finish

	return retval

# get events from each user postd in name-id file
# stored them in a file by modifying the xml stream properly (?how)
	# option: record only the events with mood-id
namedict = {};
namecrawltime = {};

# get the latest name2id file and crawl the events of the user names there
# todo: need to keep a marker of what have been crawled for the user

# DEBUG:
#lj_getevents("bidbt", 0, "")
#quit()

iters = 0;
while 1:
	# load the latest name2id file
	for dirname, dirnames, filenames in os.walk('../data/names/'):
		#filenames.sort();
		nameid_file =  os.path.join(dirname, filenames[len(filenames)-1])
		print(nameid_file)
		f = open(nameid_file)
		i = 0;
		for line in f:
			items = line.strip().split('|')
			##print(items[0], items[1], "_"
			# insert to dictionary if does not exist
			# key: username, value: index
			if items[1] in namedict:
				index = namedict[items[1]]
				if (index != items[0]):
					print("fatal error! nameid file and dictionary does not match")
					quit()
			else:
				namedict[items[1]] = items[0]

			# beforedate for syncitems
			if len(items) == 3:
				namecrawltime[items[1]] = items[2]
			else:
				namecrawltime[items[1]] = ""

			i = i + 1
			#if i == 10:
			#	break;
		f.write

	# update events and friends
	items = nameid_file.split('_');
	index = int(items[1]); # global iteration read from file system

	# data directory
	if not os.path.exists("../data/events/%010d/" % (index)):
    		os.makedirs("../data/events/%010d/" % (index))

	userind = 1
	for key in namedict.keys():
		print("crawling [%d]" % (userind),)
		print(key, namedict[key],)

		outpath = "../data/events/%010d/%s_%010d.xml" % (index,key,index)
		# getevents if there's more the crawl
		# TODO: if the file exists, do nothing
		if  namecrawltime[key] != "done" and not os.path.exists(outpath):
			eventtime = lj_getevents(key, index, namecrawltime[key])
			#print(eventtime
			if eventtime == "":
				namecrawltime[key] = "done";
			else:
				namecrawltime[key] = eventtime;

			# be a nice bot/crawler!
			sleep(0.2)

		userind = userind + 1
		# getfriends if this is the new run (iters == 0)
		# expand the user base!
		#if iters == 0:
		#	friends = lj_getfriends(key)
		#	for friend in friends:
		#		if friend not in namedict:
		#			namedict[friend] = len(namedict)+1
		#			namecrawltime[friend] = ""
		#	# be a nice bot/crawler!
		#	sleep(0.2)

	#break;
	# flush out to a new name2id
	items = nameid_file.split('_');
	index = int(items[1]) + 1;
	nameid_file2 = "%s_%010d" % (items[0], index)
	print("\nupdating name2id file:", nameid_file2)
	f = open(nameid_file2, "w+")
	for key in namedict.keys():
		output = str(namedict[key])+"|"+key+"|"+namecrawltime[key]+"\n"
		f.write(output)

	break;

	iters = iters + 1;

#	if iters == 10:
#		break;
