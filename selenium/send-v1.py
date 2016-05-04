#!/usr/bin/env python3
#coding: utf-8

import sys
import random
import subprocess

QQfile = sys.argv[1]
mailfile = "/root/mail_from.txt"
zpseed = "/root/zpseed.txt"
template_file = "/root/template.txt"
i = 0

command = '''python sendmail-v1.py -m %s -n "%s" -t %s -i 10.2.17.23 -s "%s" -f %s'''

fpm = open(mailfile, 'rb')
from_list = fpm.readlines()
fpm.close()

fpz = open(zpseed, 'rb')
zpseed_list = fpz.readlines()
fpz.close()

fpt = open(template_file, 'rb')
template_list = fpt.readlines()
fpt.close()

fp = open(QQfile, 'rb')
for QQ in fp:
    if QQ in zpseed_list:
        continue
    i+=1
    mail_from = random.choice(from_list).strip()
    template = random.choice(template_list).strip().split('=>')
    from_name = template[0]
    subject = template[1]
    htmlfile = template[2]
    # print command % (mail_from, from_name, QQ.strip(), subject, htmlfile)
    subprocess.call(command % (mail_from, from_name, QQ.strip(), subject, htmlfile), shell=True)
    if i == 99:
	# print i
    	subprocess.call(command % ("wenji@heyi.com", "文学", "2015@qq.com", "怎样才能突破自己的底线", "duanwen1.html"), shell=True)
	i = 0

fp.close()
