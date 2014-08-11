'''
Created on 2012-11-21

@author: holen
'''
import MySQLdb as db_helper;
import parsexml as parsexml

login_info = parsexml.printxmldata("sewcloud")
mdb_user = login_info['user']
mdb_pass = login_info['passwd']
mdb_ip = login_info['ip']

global_db_name  = "globalDB_0";
mesher_db_name  = "carrierDB_0";
report_db_name  = 'reportDB_0';
archive_db_name = 'archiveDB_0';
list_db_name    = 'listDB_0';
resourcedb_name    = 'resource_db';
admin_db_name    = 'adminDB_0';

global_db_host  = mdb_ip
resourcedb_host  = mdb_ip
bounce_db_host  = mdb_ip
list_db_host    = mdb_ip
report_db_host  = mdb_ip
archive_db_host = mdb_ip
admin_db_host = mdb_ip

def get_global_conn():
    return db_helper.connect(global_db_host, mdb_user, mdb_pass, global_db_name, charset='utf8');

def get_admin_conn():
    return db_helper.connect(admin_db_host, mdb_user, mdb_pass, admin_db_name, charset='utf8');

def get_resource_conn():
    return db_helper.connect(resourcedb_host, mdb_user, mdb_pass, resourcedb_name);

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


def exe_update_sql(conn, sql="select 1", use_dict=False, close=False, executemany=False, args=None):
    
    cursor = conn.cursor(db_helper.cursors.DictCursor) if use_dict else conn.cursor();
    try:
        if(executemany):
            cursor.executemany(sql, args);
            conn.commit()
            return cursor._info
        else:
            cursor.execute(sql);
            conn.commit()
            return cursor._info
    except Exception,e:
        conn.rollback()
        print e 
    
    cursor.close();
    if(close) : 
        conn.close();
        
def exe_sql_with_p(conn, sql="select 1", params = None, use_dict=False, close=False):
    cursor = conn.cursor(db_helper.cursors.DictCursor) if use_dict else conn.cursor();
    cursor.execute(sql, params);
    result = cursor.fetchall();
    cursor.close();
    
    if(close) : 
        conn.close();
        
    return result;

def close_conn(conn):
    conn.close();
