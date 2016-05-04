#-* coding:UTF-8 -*
#!/usr/bin/env python

#coding=UTF-8
'''
Created on 2014-4-17

@author: holen
'''

import mdb as mdb
import sys
import getcid as gcid
import getmid as gmid


def exportList(cid, list_id):
    sql_str = '''
        select
            email
        from
            l%s_subscriber
        into outfile
            '%s'
    '''
    list_conn = mdb.get_list_conn(cid)
    mdb.exe_sql(list_conn, sql_str % (list_id, filename), False, True)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("Export List\nUsage: python %s list_id" % sys.argv[0])
            sys.exit()
        list_id = sys.argv[1]
        mid = gmid.getmid(list_id)
        cid = gcid.getcid(mid)
        filename = "/tmp/%s.txt" % list_id
        exportList(cid, list_id)
    else:
        print("Export List\nUsage: python %s list_id" % sys.argv[0])
        sys.exit()
