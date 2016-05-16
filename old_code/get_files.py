# script that downloads all as many files as possible from live journal 
# and stores them in a folder named downloads
from os import popen
import time
import os
import subprocess
import shlex
from lxml import etree
from time import sleep
from xmltest import get_posts
from xmltest import to_file

username = 'bidbt'#'kenghao'#
password = 'bid35460'#'smallcat1003'#


def startXMLStr():
    return '<?xml version=\\"1.0\\"?><methodCall>'

def appendModule(xml, modName):
    return xml+'<methodName>'+modName+'</methodName><params><param><value><struct>'

def endXmlStr(xml):
    return xml + '<member><name>ver</name><value><int>1</int></value></member></struct></value></param></params></methodCall>'

def appendParamMember(xml, name, val, valtype):
    return xml+'<member><name>'+name+'</name><value><'+valtype+'>'+val+'</'+valtype+'></value></member>'

# modified lj_getevents to return the filename of the target user 
# which I can then pass in my get_posts method
def lj_getevents(target_user, index, beforedate):
    xml = startXMLStr();
    xml = appendModule(xml, 'LJ.XMLRPC.getevents');
    xml = appendParamMember(xml, 'username', 'bidbt', 'string');
    xml = appendParamMember(xml, 'password', 'bid35460', 'string');
    xml = appendParamMember(xml, 'selecttype', 'lastn', 'string');
    xml = appendParamMember(xml, 'howmany', '1000', 'int');
    xml = appendParamMember(xml, 'usejournal', target_user, 'string');
    xml = endXmlStr(xml);
    curl = 'curl -d "'+xml+'" http://www.livejournal.com/interface/xmlrpc'
    pp = subprocess.Popen(shlex.split(curl),stdout=subprocess.PIPE)
    content = pp.communicate()[0]
    print(len(content))
    # Checks that the downloaded file is not an error message
    if len(content) > 371:
	    f = open("../downloads/" + target_user + ".xml", 'wb')
	    f.write(content)
	    f.close()
	
	# * files with the error message that the posting limit has been 
	# * exceeded are 371 bytes long
	# * The program sleeps for an hour after it gets such a file
    elif len(content) == 371:
         sleep(3600)
    docName =  str(target_user)
    return docName

# maps username to id (String to String)
namedict = {};
# maps username to empty string (probably cause he is not using the beforedate)
namecrawltime = {};

iters = 0;
# load the name2id file
f = open("../data/names/name2id_0")
for line in f:
	items = line.strip().split('|')
	namedict[items[1]] = items[0]


userind = 1
for key in namedict.keys():
	print (key, namedict[key])

	#puts all the files it downloads in the downloads folder
	outpath = "./downloads"
	
	# start a fresh crawl
	f = open(outpath, "a")	
	tic = time.clock()	
	eventtime = lj_getevents(key, "", f)
	toc = time.clock()
	if toc-tic < 0.2:
		sleep(0.2-toc+tic)
	f.close()

# def get_usernames():
#     i = 0
#     for dirname, dirnames, filenames in os.walk('../data/names/'):
#         nameid_file =  os.path.join(dirname, filenames[len(filenames)-1])
#         print(nameid_file)
#         f = open(nameid_file)
#         iters = 0
#         for line in f:
#             items = line.strip().split('|')
#             if items[1] in namedict:
#                 index = namedict[items[1]]
#                 if (index != items[0]):
#                     print("fatal error! nameid file and dictionary does not match")
#                     quit()
#             else:
#                 namedict[items[1]] = items[0]

#             if len(items) == 3:
#                 namecrawltime[items[1]] = items[2]
#             else:
#                 namecrawltime[items[1]] = ""
#             iters += 1
#             index = int(namedict[items[1]]) # global iteration read from file system
#         i = i + 1
#     return namedict, namecrawltime

