'''
Created on 2012-11-21

@author: woo
'''
import MySQLdb as db_helper;
from datetime import datetime, time, timedelta;


mdb_user = "root"
mdb_pass = "EpCAre123"

global_db_name  = "globalDB_0";
mesher_db_name  = "carrierDB_0";
archive_db_name = 'archiveDB_0';
list_db_name    = 'listDB_0';

global_db_host  = "10.1.1.244";
bounce_db_host  = "10.1.1.248";
list_db_host    = "10.1.1.202";
report_db_host  = "10.1.1.247";
archive_db_host = "10.1.1.247"

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
    return db_helper.connect(report_db_host, mdb_user, mdb_pass, report_db_name[0]['db_name'], charset='gb2312');

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