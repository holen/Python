'''
Created on 2012-11-21

@author: z
'''
import MySQLdb as db_helper;
import parsexml as parsexml

login_info = parsexml.printxmldata("sewcloud")
mdb_user = login_info['user']
mdb_pass = login_info['passwd']
mdb_ip = login_info['ip']

global_db_name  = "globalDB_0";
mesher_db_name  = "carrierDB_0";
archive_db_name = 'archiveDB_0';
list_db_name    = 'listDB_0';

global_db_host  = mdb_ip
bounce_db_host  = mdb_ip
list_db_host    = mdb_ip
report_db_host  = mdb_ip
archive_db_host = mdb_ip

vmware_host = "192.168.1.117"
vmware_name = "globalDB_0"
day_report_host = "192.168.1.222"
day_report_name = "yulin"

def get_vmware_conn():
    return db_helper.connect(vmware_host, 'root', 'qwer1234', vmware_name, charset='utf8');

def get_error_conn():
    return db_helper.connect(day_report_host, 'report', 'qwer1234', day_report_name, charset='utf8');

def get_global_conn():
    return db_helper.connect(global_db_host, mdb_user, mdb_pass, global_db_name, charset='utf8');

def get_mesher_conn():
    return db_helper.connect(global_db_host, mdb_user, mdb_pass, mesher_db_name, charset='utf8');

def get_archive_conn():
    return db_helper.connect(archive_db_host, mdb_user, mdb_pass, archive_db_name, charset='utf8');

def get_report_conn(client_id):
    get_reportdb_sql = '''
        select 
            d.db_name
        from 
            client c,db d 
        where 
            c.reporter_db_id=d.db_id and c.client_id = %s
    '''

    global_conn = get_global_conn();
    report_db_name = exe_sql(global_conn, get_reportdb_sql % (client_id), True, True);
    # return db_helper.connect(report_db_host, mdb_user, mdb_pass, report_db_name[0]['db_name'], charset='gb2312');
    return db_helper.connect(report_db_host, mdb_user, mdb_pass, report_db_name[0]['db_name'], charset='utf8');

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


def exe_insert_sql(conn, sql="select 1", use_dict=False, close=True):
    
    cursor = conn.cursor()
    cursor.execute(sql);
    conn.commit()
    
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
