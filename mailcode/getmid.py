#-* coding:UTF-8 -*
#!/usr/bin/env python

#coding=UTF-8
'''
Created on 2014-4-17

@author: holen
'''

import mdb as mdb
import sys


def getmid(lid):
    sql_str = '''
        select
            message_id
        from
            message_list ml
        where
            ml.list_id = %s
        '''
    global_conn = mdb.get_global_conn()
    message_id = mdb.exe_sql(global_conn, sql_str % lid, False, True)
    return message_id[0][0]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("根据list id查询message id\nUsage: python %s list_id" % sys.argv[0])
            sys.exit()
        print getmid(sys.argv[1])
    else:
        print("根据list id查询message id\nUsage: python %s list_id" % sys.argv[0])
        sys.exit()
