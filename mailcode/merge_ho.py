#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys
import MySQLdb
import getcid as gcid
import getReportdb_id as grid
import parsexml as parsexml

login_info = parsexml.printxmldata("sewcloud")
mdb_user = login_info['user']
mdb_pass = login_info['passwd']
mdb_ip = login_info['ip']

def merge_ho_ct(d_cid, d_mid, s_cid, s_mid):
    insert_ho_sql = '''
        INSERT INTO 
            msg_%s_%s_ho (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`, `op_system`, `browser`) 
        select 
            `unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`, `op_system`, `browser` 
        from 
            %s.msg_%s_%s_ho ;
    '''

    insert_ct_sql = '''
        INSERT INTO 
            `msg_%s_%s_ct` (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `url_id`, `url_value`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`) 
        select 
            `unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `url_id`, `url_value`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`
        from 
            %s.msg_%s_%s_ct ;
    '''

    # report_conn = mdb.get_report_conn(d_cid)
    # report_conn = MySQLdb.connect( host='10.10.11.202', user='epcare', passwd='EpCAre!@#', db='reportDB_new' )
    reportdb = grid.get_report_conn(d_cid)
    report_conn = MySQLdb.connect( host= mdb_ip, user= mdb_user, passwd= mdb_pass, db=reportdb ,charset='utf8')
    cursor = report_conn.cursor()
    # reportdb = 'reportDB_new'
    print insert_ho_sql % (d_cid, d_mid, reportdb, s_cid, s_mid)
    print insert_ct_sql % (d_cid, d_mid, reportdb, s_cid, s_mid)
    cursor.execute(insert_ho_sql % (d_cid, d_mid, reportdb, s_cid, s_mid))
    cursor.execute(insert_ct_sql % (d_cid, d_mid, reportdb, s_cid, s_mid))
    report_conn.commit()
    cursor.close()
    report_conn.close()
    # mdb.exe_insert_sql(report_conn, insert_ho_sql % (d_cid, d_mid, reportdb, s_cid, s_mid), True, True)
    # mdb.exe_insert_sql(report_conn, insert_ct_sql % (d_cid, d_mid, reportdb, s_cid, s_mid), True, True)

if __name__ == '__main__':
    if len(sys.argv) == 3 :
        if sys.argv[1] == '-h':
            print("合并报表\nUsage: python %s dest_message_id src_message_id" % sys.argv[0]);
            sys.exit()
        d_cid = gcid.getcid(int(sys.argv[1]))
        d_mid = sys.argv[1]
        s_cid = gcid.getcid(int(sys.argv[2]))
        s_mid = sys.argv[2]
        merge_ho_ct(d_cid, d_mid, s_cid, s_mid) 
    else :
        print("合并报表\nUsage: python %s dest_message_id src_message_id" % sys.argv[0]);
        sys.exit()
