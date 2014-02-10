import MySQLdb as db_helper;
from datetime import datetime, time, timedelta;
# get_bouncedb_sql = '''
# 	select 
# 		d.db_name,c.branch_id
# 	from 
# 		client c,db d 
# 	where 
# 		c.bounce_db_id=d.db_id and c.branch_id = 3
# '''
get_bouncedb_sql = '''
	select 
		distinct d.db_name,c.branch_id
	from 
		client c,db d 
	where 
		c.bounce_db_id=d.db_id
'''

global_db_host  = "10.1.1.244";
global_db_name  = "globalDB_0";
mdb_user = "root"
mdb_pass = "EpCAre123"

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
