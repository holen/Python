#-* coding:UTF-8 -*
#!/usr/bin/env python

#coding=UTF-8
'''
Created on 2015-11-30

@author: holen
'''

import mdb as mdb
import sys

def getipid_city(city):
    sql_str = "select place_id from ip_place ip where city='%s' order by place_id limit 1 "
    global_conn = mdb.get_global_conn();
    ip_place_id = mdb.exe_sql(global_conn, sql_str % city, False, True)
    return ip_place_id[0][0]

def getipid_province(province):
    sql_str = "select place_id from ip_place ip where province='%s' order by place_id limit 1"
    global_conn = mdb.get_global_conn();
    ip_place_id = mdb.exe_sql(global_conn, sql_str % province, False, True)
    return ip_place_id[0][0]

if __name__ == '__main__':
	pass
    #getipid_city('厦门市')
    #getipid_province('北京')
