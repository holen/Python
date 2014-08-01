#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys
import MySQLdb
import getcid as gcid
import getReportdb_id as grid
import common.mdb as mdb
import string, random
import parsexml as parsexml

login_info = parsexml.printxmldata("sewcloud")
mdb_user = login_info['user']
mdb_pass = login_info['passwd']
mdb_ip = login_info['ip']

def insert_ho_ct(cid, mid, action_time, ho_num, ct_num):
    domain_name = 'qq.com'
    insert_ho_sql = '''INSERT INTO msg_%s_%s_ho (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`, `op_system`, `browser`) values ''' % (cid, mid)
    insert_ho_sql += '''( %s, %s, 35811, 2, %s, 1, %s, %s, %s, '58.23.3.163', 974586787, 214, '中国', '福建', '厦门市', NULL, 'Windows 7', 'Unknown' );'''
    insert_ct_sql = '''INSERT INTO msg_%s_%s_ct (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `url_id`, `url_value`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`) values ''' % (cid, mid) 
    insert_ct_sql += '''(%s, %s, 35811, 2, %s, 1, %s, %s, %s, %s, %s, '58.23.3.163', 974586787, 214, '中国', '福建', '厦门市', NULL );'''

    reportdb = grid.get_report_conn(cid)
    report_conn = MySQLdb.connect( host=mdb_ip, user=mdb_user, passwd=mdb_pass, db=reportdb ,charset='utf8')
    cursor = report_conn.cursor()
    url = geturl(mid)
    url_id = url['url_id']
    url_value = (url['value']).encode('utf-8')
    ho_args_list = []
    src_data = src_ho_ct(mid)
    src_ho = int(src_data['dist_opens'])
    src_ct = int(src_data['dist_url_clicks'])
    if src_ho >= ho_num:
        ho_diff = 1
    else:
        ho_diff = ho_num - src_ho
    if src_ct >= ct_num:
        ct_diff = 1
    else:
        ct_diff = ct_num - src_ct
    for i in range(ho_diff):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
        email_address = 'ep_00%s@qq.com' % i
        ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time))
    ct_args_list = []
    for i in range(int(ct_diff)):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
        email_address = 'ep_00%s@qq.com' % i
        ct_args_list.append((unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time))
    try:
    #    for i in range(int(ho_num)):
    #        email_address = 'ep_%s@qq.com' % i
    #        ho_sql = insert_ho_sql % (cid, mid, mid, cid, email_address, domain_name, action_time) 
    #        cursor.execute(ho_sql)
    #    for i in range(int(ct_num)):
    #        email_address = 'ep_%s@qq.com' % i
    #        ct_sql =  insert_ct_sql % (cid, mid, mid, cid, email_address, domain_name, url_id, url_value, action_time)
    #        cursor.execute(ct_sql)
        cursor.executemany(insert_ho_sql, ho_args_list)
        cursor.executemany(insert_ct_sql, ct_args_list)
        report_conn.commit()
    except Exception,e:
        report_conn.rollback()
        print e
    cursor.close()
    report_conn.close()

def geturl(mid):
    sql = '''
        select url_id, value from track_url t where t.message_id = %s limit 1 
    '''
    global_conn = mdb.get_global_conn()
    data = mdb.exe_sql(global_conn, sql % (mid), True, True)
    return data[0]

def src_ho_ct(mid):
    sql = '''select dist_opens, dist_url_clicks from message m where m.message_id = %s'''
    global_conn = mdb.get_global_conn()
    data = mdb.exe_sql(global_conn, sql % (mid), True, True)
    return data[0]

if __name__ == '__main__':
    if len(sys.argv) == 5 :
        if sys.argv[1] == '-h':
            print("插入ho、ct数据\nUsage: python %s mid action_time ho_num ct_num" % sys.argv[0]);
            sys.exit()
        cid = gcid.getcid(int(sys.argv[1]))
        mid = sys.argv[1]
        action_time = sys.argv[2]
        ho_num = sys.argv[3]
        ct_num = sys.argv[4]
        while True:
            flag = raw_input("Are you when to update message:%s to dist_opens=%s and dist_url_clicks=%s, Please input [y/n]: " % (mid, ho_num, ct_num)) 
            if flag == 'y':
                insert_ho_ct(cid, mid, action_time, int(ho_num), int(ct_num))
                print "Done! Update message:%s dist_opens=%s dist_url_clicks=%s" % (mid, ho_num, ct_num) 
                break
            elif flag == 'n':
                print "Nothing is dode !"
                break
            else:
                print "Please input y/n "
    else :
        print("插入ho、ct数据\nUsage: python %s mid action_time ho_num ct_num" % sys.argv[0]);
        sys.exit()
