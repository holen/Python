#/usr/bin/python
'''
	create by holen 2013-3-7
	This shell is for adjust the message priority
'''
import MySQLdb 
from datetime import datetime, time, timedelta
import sys

mdb_user = "root"
mdb_pass = "EpCAre123"
global_db_name  = "globalDB_0"
global_db_host  = "10.1.1.244"
today = datetime.combine(datetime.today(), time(0, 0))
tomorrow = today + timedelta(days=1)

def get_global_conn():
    return MySQLdb.connect(global_db_host, mdb_user, mdb_pass, global_db_name, charset='utf8');

def exe_sql(conn, sql="select 1", use_dict=False, close=False):
    
    cursor = conn.cursor(MySQLdb.cursors.DictCursor) if use_dict else conn.cursor();
    cursor.execute(sql);
    result = cursor.fetchall();
    
    cursor.close();
    if(close) : 
        conn.close();
        
    return result;

def close_conn(connection):
    connection.close();

get_message_sql = '''
	select 
		group_concat(m.message_id) 
	from 
		message m
 	where 
 		m.schedule_time between '%s' and '%s' and m.status_id < 50
 	order by 
 		m.schedule_time ;
'''

global_conn = get_global_conn();
message_ids = exe_sql(global_conn, get_message_sql % (today, tomorrow), False, True)

if message_ids[0][0] :
	messages = message_ids[0][0].split(',')

	update_pri_sql = '''
			update message m set m.priority = %s where m.message_id = %s ;commit;
		'''

	update_conn = get_global_conn()

	i = 0

	for message in messages:
		i=i+10
		if(i < 127):
			result = exe_sql(update_conn, update_pri_sql % (int(i), int(message)), False, False)	
		else:
			result = exe_sql(update_conn, update_pri_sql % (127, int(message)), False, False)

	if update_conn:
	    close_conn(update_conn);
else:
	sys.exit(0)
