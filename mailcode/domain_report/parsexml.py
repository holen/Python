#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys
from  xml.dom import  minidom

def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename='/etc/sewcloud.xml'):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')

def get_xml_data(filename='/etc/sewcloud.xml'):
    doc = minidom.parse(filename) 
    root = doc.documentElement

    machine_nodes = get_xmlnode(root,'machine')
    machine_list=[]
    for node in machine_nodes: 
        machine_name = get_attrvalue(node,'name') 
        machine_ip = get_xmlnode(node,'ip')
        machine_user = get_xmlnode(node,'user')
        machine_passwd = get_xmlnode(node,'password')

        #machine_ip = get_nodevalue(machine_ip[0]).encode('utf-8','ignore')
        machine_ip = get_nodevalue(machine_ip[0]).encode('utf-8','ignore')
        machine_user = get_nodevalue(machine_user[0])
        machine_passwd = get_nodevalue(machine_passwd[0]).encode('utf-8','ignore')
        machine = {}
        machine['name'] , machine['ip'] , machine['user'] , machine['passwd'] = (
            machine_name, machine_ip , machine_user , machine_passwd
        )
        machine_list.append(machine)
    return machine_list

def test_xmltostring():
    print xml_to_string()

def printxmldata(machine_name):
    machine_list = get_xml_data()
    for machine in machine_list :
        if machine['name'] == machine_name :
            return machine
            #print machine['name'], machine['ip'], machine['user'], machine['passwd']

if __name__ == "__main__":
    #test_xmltostring()
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print "Usage: python %s machine_name " % sys.argv[0]
        else:
            machine_name = sys.argv[1]
            print printxmldata(machine_name)
    else:
        print "Usage: python %s machine_name " % sys.argv[0]
        sys.exit()
