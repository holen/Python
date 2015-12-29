#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import sys

def getIPAddFromFile(fobj):
    regex = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', re.IGNORECASE)
    ipadds = re.findall(regex, fobj)
    print ipadds
    return ipadds

def getPhoneNumFromFile(fobj):
    regex = re.compile(r'1\d{10}', re.IGNORECASE)
    phonenums = re.findall(regex, fobj)
    print phonenums
    return phonenums

def getMailAddFromFile(fobj):
    regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)
    mails = re.findall(regex, fobj)
    for mail in mails:
	print mail
    return mails

def getUrlFromFile(fobj):
    regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)
    urls = regex.findall(fobj)
    print urls
    return urls

def main(FilefilePath):
    fobj = open(FilefilePath, 'rb').read()
    #urllist = getUrlFromFile(fobj)
    mailList = getMailAddFromFile(fobj)
    #phoneNum = getPhoneNumFromFile(fobj)
    #ipaddlist = getIPAddFromFile(fobj)

if __name__ == '__main__':
    main(sys.argv[1])
