#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert ip 2 to 10 or convert ip 10 to 2

import os,sys,csv

# global definition
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

# bin2dec
# 二进制 to 十进制: int(str,n=10) 
def bin2dec(string_num):
    print str(int(string_num, 2))

# dec2bin
# 十进制 to 二进制: bin() 
def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        # print num, rem
        mid.append(base[rem])

    binary=''.join([str(x) for x in mid[::-1]])
    if len(binary) == 8:
    	return binary;
    else:
    	i = 8 - len(binary)
    	binary = '%s%s' % ('0'*i, binary)
    	return binary;
    	

# convert ip 10 to 2
def convert(ip):
	iplist = ip.split('.')
	array = []
	for field in iplist:
		array.append(dec2bin(field))
	else:
		print ' '.join([str(x) for x in array[::]])

# convert('119.163.252.40')
# bin2dec('1110')

f = open('C:\\Users\\huilong.zhang\\Desktop\\ip.csv', 'rb')
data = f.readlines()
f.close()
for eachLine in data:
	print eachLine.strip(),',', convert(eachLine.strip())

