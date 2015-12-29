#-* coding:UTF-8 -*
#!/usr/bin/env python

#coding=UTF-8
'''
Created on 2014-4-17

@author: holen
'''

import mdb as mdb
import sys

def getcid(mid):
    sql_str = '''
        select 
            m.client_id, c.client_name
        from 
            message m, client c
        where 
            m.client_id = c.client_id and m.message_id = %s
        '''
    global_conn = mdb.get_global_conn();
    client_id = mdb.exe_sql(global_conn, sql_str % mid, False, True)
    return client_id[0][0]

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-h':
            print("根据邮件id查询客户id\nUsage: python %s message_id " % sys.argv[0]);
            sys.exit()
        print getcid(sys.argv[1])
    else :
        print("根据邮件id查询客户id\nUsage: python %s message_id " % sys.argv[0]);
        sys.exit()
