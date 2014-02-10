#!/usr/bin/python
#coding=UTF-8
import MySQLdb as db_helper;
from datetime import datetime, time, timedelta;
import codecs

mdb_user = "root"
mdb_pass = "EpCAre123"
bounce_db_host  = "10.1.1.248";
global_db_host  = "10.1.1.244";
global_db_name  = "globalDB_0";

get_bouncedb_sql = '''
	select 
		d.db_name
	from 
		client c,db d 
	where 
		c.bounce_db_id=d.db_id
		and c.client_id in 
		(select m.client_id from message m where m.message_id = %s)
	'''

global_conn = db_helper.connect(global_db_host, mdb_user, mdb_pass, global_db_name, charset='utf8')

def exe_sql(conn, sql="select 1", use_dict=False, close=False):
    
    cursor = conn.cursor(db_helper.cursors.DictCursor) if use_dict else conn.cursor();
    cursor.execute(sql);
    result = cursor.fetchall();
    
    cursor.close();
    if(close) : 
        conn.close();
        
    return result;
 
def get_bouncedb():
	bounce_db = exe_sql(global_conn, get_bouncedb_sql % (10109), True, True)
	return bounce_db
 
bounce_db_name = get_bouncedb()
bounce_conn = db_helper.connect(bounce_db_host, mdb_user, mdb_pass, bounce_db_name[0]['db_name'], charset='utf8');

get_error_sql = '''
	select 
		h.real_from,h.from_ip,h.error,count(0) as count 
	from 
		msg_3156_10109_h h 
	where 
		h.return_type_id = 2 and domain_name = '%s'
	group by 
		h.error 
	order 
		by count desc
	'''

def get_error():
	error = exe_sql(bounce_conn, get_error_sql % ('qq.com'), True, True)
	return error


