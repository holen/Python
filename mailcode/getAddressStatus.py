#!/usr/bin/python
#coding=UTF-8
'''
Created on 2014-05-09

@author: holen
'''
import sys
import mdb as mdb
import getcid as gcid

def get_bounceinfo(cid, mid, email=None, test = False):
	get_data = '''
		select 
			*
		from 
			msg_%s_%s_h h 
		where
			h.email = '%s'
	'''

	get_test_data = '''
		select 
			*
		from 
			msg_tester_result mr 
		where
			mr.message_id = %s 
	'''

        if email :
            get_test_data += " and mr.email_address = '%s'" % (email) 

        if test :
            sql = get_test_data % (mid)
            global_conn = mdb.get_global_conn()
            datas = mdb.exe_sql(global_conn, sql, True, True)
        else :
            sql = get_data % (cid, mid, email)
            bounce_conn = mdb.get_bounce_conn(cid);
            datas = mdb.exe_sql(bounce_conn, sql, True, True)

        # print datas
        for data in datas:
            for key,values in data.iteritems():
                print '%-20s    %s' %(key, values)
            print '-'*50

if __name__ == '__main__':
        if len(sys.argv) == 2 :
            if sys.argv[1] == '-h':
                print("查询一个邮件地址(测试)的发送情况\nUsage: python %s message_id email_address [test] " % sys.argv[0]);
                sys.exit()
            get_bounceinfo(gcid.getcid(int(sys.argv[1])), sys.argv[1], None, True)
        elif len(sys.argv) == 3 :
            get_bounceinfo(gcid.getcid(int(sys.argv[1])), sys.argv[1], sys.argv[2], False)
        elif len(sys.argv) == 4 and sys.argv[3] == 'test' :
            get_bounceinfo(1, sys.argv[1], sys.argv[2], True)
        else :
            print("查询一个邮件地址(测试)的发送情况\nUsage: python %s message_id email_address [test] " % sys.argv[0]);
            sys.exit()

