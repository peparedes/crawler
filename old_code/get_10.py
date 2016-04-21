# scrpit thatgets the first 10 users from the name2id_0 file 
# and creates a file of their posts 
from os import popen
import os
import subprocess
import shlex
from lxml import etree
from time import sleep
from xmltest import get_posts
from xmltest import to_file

# crawler account
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
    xml = appendParamMember(xml, 'username', username, 'string');
    xml = appendParamMember(xml, 'password', password, 'string');
    xml = appendParamMember(xml, 'selecttype', 'lastn', 'string');
    xml = appendParamMember(xml, 'howmany', '50', 'int');
    xml = appendParamMember(xml, 'usejournal', target_user, 'string');
    if beforedate != "":
        xml = appendParamMember(xml, 'beforedate', beforedate, 'string');
    xml = endXmlStr(xml);

    curl = 'curl -d "'+xml+'" http://www.livejournal.com/interface/xmlrpc'
    pp = subprocess.Popen(shlex.split(curl),stdout=subprocess.PIPE)
    content = pp.communicate()[0]
    docName = "../data/events/%010d/%s_%010d.xml" % (int(index) ,target_user, int(index))
    f = open(docName, 'w+')
    f.write(content.decode("utf-8"))
    f.close()
    return docName

# maps username to id (String to String)
namedict = {};
# maps username to empty string (probably cause he is not using the beforedate)
namecrawltime = {};

# returns tuple with namedict and namecrawltime
def get_10_usernames():
    i = 0
    for dirname, dirnames, filenames in os.walk('../data/names/'):
        if i == 1:
              break;
        nameid_file =  os.path.join(dirname, filenames[len(filenames)-1])
        print(nameid_file)
        f = open(nameid_file)
        iters = 0
        for line in f:
            if iters == 10:
                break;

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
            iters += 1
            index = int(namedict[items[1]]) # global iteration read from file system

            if not os.path.exists("../data/events/%010d/" % (index)):
                os.makedirs("../data/events/%010d/" % (index))
        i = i + 1
    return namedict, namecrawltime


# dictionary done
tup = get_10_usernames()
namedict = tup[0]
namecrawltime = tup[1]

# for username in namedict.keys():
#     to_file(get_posts(lj_getevents(username, namedict[username], namecrawltime[username])))






