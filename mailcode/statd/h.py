#!/usr/bin/python
#coding=UTF-8
'''
Created on 2012-3-11

@author: jlcoa
'''
import MySQLdb as db_helper;
import time;
from datetime import datetime, time, date, timedelta;
import codecs

mdb_user = "root"
mdb_pass = "EpCAre123"

global_db_name  = "globalDB_0";
mesher_db_name  = "carrierDB_0";
report_db_name  = 'reportDB_0';
archive_db_name = 'archiveDB_0';
list_db_name    = 'listDB_0';

global_db_host  = "10.1.1.244";
bounce_db_host  = "10.1.1.248";
list_db_host    = "10.1.1.202";
report_db_host  = "10.1.1.203";
archive_db_host = "10.1.1.247"


def get_global_conn():
	return db_helper.connect(global_db_host, mdb_user, mdb_pass, global_db_name, charset='utf8');

def get_mesher_conn():
	return db_helper.connect(global_db_host, mdb_user, mdb_pass, mesher_db_name, charset='utf8');

def get_archive_conn():
	return db_helper.connect(archive_db_host, mdb_user, mdb_pass, archive_db_name, charset='utf8');

def get_report_conn():
	return db_helper.connect(report_db_host, mdb_user, mdb_pass, report_db_name, charset='utf8');

def get_bounce_conn(client_id):
	get_bouncedb_sql = '''
		select 
			d.db_name
		from 
			client c,db d 
		where 
			c.bounce_db_id=d.db_id and c.client_id = %s
	'''

	global_conn = get_global_conn();
	bounce_db_name = exe_sql(global_conn, get_bouncedb_sql % (client_id), True, True);
	return db_helper.connect(bounce_db_host, mdb_user, mdb_pass, bounce_db_name[0]['db_name'], charset='utf8');

def exe_sql(conn, sql="select 1", use_dict=False, close=False):
    
    cursor = conn.cursor(db_helper.cursors.DictCursor) if use_dict else conn.cursor();
    cursor.execute(sql);
    result = cursor.fetchall();
    
    cursor.close();
    if(close) : 
        conn.close();
        
    return result;

def close_conn(conn):
    conn.close();

def statd():
	
	find_msg_sql = """
		select 
			DATE_FORMAT(m.schedule_time, '%%m-%%d') as day, m.client_id, group_concat(m.message_id) as messages
		from 
			message m
		where 
			m.schedule_time between '%s' and '%s'
		group by 
			day, m.client_id
		order by
			day asc
	""";
		
	global_conn = get_global_conn();
	splited = exe_sql(global_conn, find_msg_sql % ('2013-2-23', '2013-2-25'), True);
	print splited

	stat_sql = '''
		select 
		   '%s' as message_id,h.domain_name, h.real_from, h.from_ip, h.to_ip, h.error, h.remark 
		from 
			msg_%s_%s_h h 
		where 
			h.return_type_id = 2
		group by 
			h.domain_name, h.error, h.remark
	'''
	
#     header = codecs.BOM_UTF8 + "日期,客户id,邮件id,域,发送域,发送ip,到达ip,error,remark"
#     print header;
	
	display = [];
	for target in splited:
		# target = splited[0];
		day = target["day"]
		client_id = target["client_id"];
		messages = target["messages"];

		bounce_conn = get_bounce_conn(client_id);

		messages = messages.split(',')
		for message in messages:
			domain_stat = exe_sql(bounce_conn, stat_sql % (message, client_id, message), True);
			display.extend(domain_stat);

		if bounce_conn:
			close_conn(bounce_conn);

	for data in display:
		print data.values()	
			
if __name__ == '__main__':
	statd();