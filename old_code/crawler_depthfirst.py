import time
import sys
from os import popen
import subprocess
import shlex
import libxml2
import os
from time import sleep
import base64

import signal



# crawler account
username = 'bidbt'
password = 'bid35460'


toquit = 0
def signal_handler(signal, frame):
	toquit = 1

def unflat(xmldoc,f, elementname, tag, tagval, isroot, rettag):
	child = xmldoc

	# eventtime in root level, or output string in recursed levels
	retval = ""
	# output string
	outstr = ""
	count = 0;
	while child is not None:

		pairs = child.children.children
		if isroot:
			#print >>f, "<%s>" % (elementname)
			outstr = outstr + "<%s>" % (elementname) 
			#print >>f, "<%s>%s</%s>" % (tag, tagval, tag)
			outstr = outstr + "<%s>%s</%s>" % (tag, tagval, tag)
			count = count + 1

		while pairs is not None:
			values = pairs.children

			name = values.content
			val = values.next.children.content
			if name != "props":
				#print >>f, "<%s>%s</%s>" % (name, values.next.children, name)
				outstr = outstr + "<%s>%s</%s>" % (name, values.next.children, name)
			else:
				#print >>f, "<props>"
				outstr = outstr + "<props>"
				outstr = outstr + unflat(values.next, f, elementname, tag, tagval, 0, "")
				outstr = outstr + "</props>"

			if isroot and name == rettag:
				retval = val
				

			pairs = pairs.next

		if isroot:
			#print >>f, "</%s>" % (elementname)
			outstr = outstr + "</%s>" % (elementname)
			
		child = child.next
	
	if isroot:
		print "\tcount:%d, oldest: %s" % (count, retval[:-1])
		print >>f, outstr, "\n"

		# make the current function atomic

		if toquit:
			quit()

		# done!
		if count < 50:
			retval = ""

	else:
		retval = outstr

	
	return retval


# parse the response
def genNewXmlForElement(f, xml, element, tag, tagval, rettag):
	doc = libxml2.parseDoc(xml)
	if doc.children.name == "html":
		# most likely server error. need to re-issue request again	
		return "again"

	root = doc.children.children.children.children.children

	# dive into the jason-like xml tree to find node to be parsed
	child = root.children
	while child is not None: 
		if child.children.content != element:
			node = child
			node.unlinkNode()
			node.freeNode()
			
		child = child.next

	child = root.children.children
	child = child.next

	# unflat jason like xml: root	
	try: 
		child = child.children.children.children
		retval = unflat(child, f, "post", tag, tagval, 1, rettag)
		# read nothing
		if retval == "":
			retval = "done"
	except:
		# something goes wrong, ok, then there's nothing written to file f
		#if doc.children.children.name == "fault":
		#	retval = "done"

		# well. let's give up
		retval = "done" 
		
	return retval
	
# xml rpc related routines
def startXMLStr():
	return '<?xml version=\\"1.0\\"?><methodCall>'

def appendModule(xml, modName):
	return xml+'<methodName>'+modName+'</methodName><params><param><value><struct>'

def endXmlStr(xml):
	return xml + '<member><name>ver</name><value><int>1</int></value></member></struct></value></param></params></methodCall>'

def appendParamMember(xml, name, val, valtype):
	return xml+'<member><name>'+name+'</name><value><'+valtype+'>'+val+'</'+valtype+'></value></member>'

# xml rpc call
def lj_getevents(target_user, beforedate, fxml):
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

	curl = '/bin/curl.exe -d "'+xml+'" http://www.livejournal.com/interface/xmlrpc'
	#print curl
	pp = subprocess.Popen(shlex.split(curl),stdout=subprocess.PIPE)
	# may cause deadlock
	#content = pp.stdout.read()
	content = pp.communicate()[0]
	pp.stdout.close()
	f = open('response.xml', 'w')
	f.write(content)
	f.close()
	#print content

	# reformat it
	retval = genNewXmlForElement(fxml, content, "events", "user", target_user, "eventtime")
	if retval == "again":
		# give it a second chance. currently, the parse fails
		retval = beforedate

	return retval


def readeventtime(xmlpath):
	f = open(xmlpath)
	content = f.read()
	f.close()
	if content[-9:] == "</posts>\n":
		# truncatng some bad tag
		#with open(xmlpath, "r+") as f:
		#	line = f.readline()
		#	while line != "</posts>\n":
		#		line = f.readline()
		#	f.truncate()
		#	f.close()

		return "done"
	else: 
		doc = libxml2.parseDoc(content + "</posts>")

		post = doc.children.children.next

		if post is None:
			return ""

		# get the last post
		eventtime = ""
		while post is not None:
			if post.name == "post":
				prevpost = post
			post = post.next


		# get the oldest eventtime
		if prevpost is not None:
			tag = prevpost.children
			while tag is not None:
				if tag.name == "eventtime":
					eventtime = tag.children.content
					break
				tag = tag.next

		return eventtime


def getXmlFilepath(name):
	outpath = "../data/events/%s/%s.xml" % (name[:2],name)
	
	# data directory
	if not os.path.exists("../data/events/%s/" % (name[:2])):
		os.makedirs("../data/events/%s/" % (name[:2]))

	return outpath


namedict = {};

#print readeventtime("../data/events/0000000000/dab-snark_0000000000.xml")
#quit()

# DEBUG:
#key = "poseidon68"
#outpath = getXmlFilepath(key)
#f = open(outpath, "w")
#print >>f, "<posts>"	
#eventtime = lj_getevents(key, "", f)
#while eventtime != "done":
#	tic = time.clock()
#	eventtime = lj_getevents(key, eventtime, f)
#	toc = time.clock()
#	if toc-tic < 0.2:
#		sleep(0.2-toc+tic)
#print >>f, "</posts>"	
#f.close()
#quit()




signal.signal(signal.SIGINT, signal_handler)

iters = 0;
# load the name2id file
f = open("../data/names/name2id_0")
for line in f:
	items = line.strip().split('|')
	namedict[items[1]] = items[0]


userind = 1
for key in namedict.keys():
	print "\ncrawling [%d]" % (userind), 
	print key, namedict[key]

	outpath = getXmlFilepath(key)
	
	# depth "crawel" 
	if not os.path.exists(outpath):
		# start a fresh crawl
		f = open(outpath, "w")
		print >>f, "<posts>"	
		eventtime = lj_getevents(key, "", f)

		closure = 1
	else:
		# read the eventtime of the oldest journal post
		eventtime = readeventtime(outpath)
		f = open(outpath, "a")
		if eventtime == "done":
			closure = 0
		else:
			closure = 1

	while eventtime != "done":
		tic = time.clock()
		eventtime = lj_getevents(key, eventtime, f)
		toc = time.clock()
		if toc-tic < 0.2:
			sleep(0.2-toc+tic)

	if closure == 1:
		print >>f, "</posts>"

	f.close()
	userind = userind + 1
