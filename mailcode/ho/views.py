#!/usr/bin/python
#coding=UTF-8
import MySQLdb as db_helper;
from datetime import datetime, time, timedelta, date;
import codecs
import os, csv
import sys
reload(sys)
sys.setdefaultencoding('gb2312')

mdb_user = "root"
mdb_pass = "EpCAre123"
report_db_host  = "10.1.1.247";
report_db_name  = ['reportDB_2', 'reportDB_0', 'reportDB_epcare', 'reportDB_lecast', 'reportDB_epedm', 'reportDB_test'];

def get_report_conn(id):
    return db_helper.connect(report_db_host, mdb_user, mdb_pass, report_db_name[id], charset='utf8');

def exe_sql(conn, sql="select 1", use_dict=False, close=False):
    
    cursor = conn.cursor(db_helper.cursors.DictCursor) if use_dict else conn.cursor();
    cursor.execute(sql);
    result = cursor.fetchall();
    
    cursor.close();
    if(close) : 
        conn.close();
        
    return result;

def get_databases():
    today = date.today()

    get_databases_sql = '''
        select 
            table_name 
        from 
            information_schema.tables 
        where 
            table_schema = '%s' and table_name like '%%_ho%%' ;
    '''
    the_file = "D:\\data.%s.csv" % (today)
    csvfile = file('%s' % (the_file), 'ab')
    writer = csv.writer(csvfile)

    for id in range(6):
        print 'report_%d start ...' % id
        report_conn = get_report_conn(id);

        databases = exe_sql(report_conn, get_databases_sql % str(report_db_name[id]), True, True)

        for database in databases:
            ho = database['table_name'].encode("utf-8")
            try:    
                datas = get_emails(id, ho)
            except Exception,e:
                continue
                print "%s is no exist ..." % (ho)
            
            writer.writerows(datas)
            print '%s is done ...' % ho

        csvfile.close();
        print 'report_%d done' %id


def get_emails(id, ho):
    get_emails_sql = '''
        select 
            ho.email_address, ho.domain_name, ho.ip, ho.country, ho.province, ho.city
        from 
            %s ho
        order by 
            ho.domain_name
    '''

    get_emails_conn = get_report_conn(id);
    emails = exe_sql(get_emails_conn, get_emails_sql % ho, False, True)
    return emails
    
if __name__ == '__main__':  
    get_databases();