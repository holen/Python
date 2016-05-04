#!/usr/bin/env python3
#coding: utf-8

import sys
import subprocess

myseed = sys.argv[1]

command = '''python check163mail.py %s %s'''

fpz = open(myseed, 'rb')

for line in fpz:
    # print line.strip().split('-----')
    username = line.strip().split('----')[0]
    password = line.strip().split('----')[1]

    # print command % (username, password)
    subprocess.call(command % (username, password), shell=True)

fpz.close()
