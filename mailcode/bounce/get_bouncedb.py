import MySQLdb as db_helper;
from datetime import datetime, time, timedelta;
import parsexml as parsexml

login_info = parsexml.printxmldata("sewcloud")
mdb_user = login_info['user']
mdb_pass = login_info['passwd']
mdb_ip = login_info['ip']

get_bouncedb_sql = '''
	select 
		distinct d.db_name,c.branch_id
	from 
		client c,db d 
	where 
		c.bounce_db_id=d.db_id
'''

global_db_host  = mdb_ip;
global_db_name  = "globalDB_0";

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
	bounce_db = exe_sql(global_conn, get_bouncedb_sql, True, True)
	return bounce_db
 
db_name = get_bouncedb()
for row in db_name:
	print row
