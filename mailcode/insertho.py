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

def insert_ho_ct(cid, mid, action_time, ho_dist_num, ho_num, ct_dist_num, ct_num):
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
    src_data = src_dist_ho_ct(mid)
    src_dist_ho = int(src_data['dist_opens'])
    src_dist_ct = int(src_data['dist_url_clicks'])
    if src_dist_ho >= ho_dist_num:
        ho_dist_diff = 1
    else:
        ho_dist_diff = ho_dist_num - src_dist_ho
    if ho_num > ho_dist_num:
        ho_diff = ho_num - ho_dist_num
    else:
        ho_diff = 1
    if src_dist_ct >= ct_dist_num:
        ct_dist_diff = 1
    else:
        ct_dist_diff = ct_dist_num - src_dist_ct
    if ct_num > ct_dist_num:
        ct_diff = ct_num - ct_dist_num
    else:
        ct_diff = 1
    ho_args_list = []
    for i in range(ho_dist_diff):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
        email_address = 'ep_00%s@qq.com' % i
        ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time))
    for i in range(ho_diff):
        unique_id = 'h6djz8c5'
        email_address = 'ep_00%s@qq.com' % i
        ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time))
    ct_args_list = []
    for i in range(int(ct_dist_diff)):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
        email_address = 'ep_00%s@qq.com' % i
        ct_args_list.append((unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time))
    for i in range(int(ct_diff)):
        unique_id = 'h6djz8c5'
        email_address = 'ep_00%s@qq.com' % i
        ct_args_list.append((unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time))
    try:
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

def src_dist_ho_ct(mid):
    sql = '''select message_id, message_name, client_id, end_time, total_count, send_count, successful_count, softbounce_count, hardbounce_count, unstart_count, html_opens, dist_opens, url_clicks, dist_url_clicks from message m where m.message_id = %s'''
    global_conn = mdb.get_global_conn()
    data = mdb.exe_sql(global_conn, sql % (mid), True, True)
    return data[0]

if __name__ == '__main__':
    if len(sys.argv) == 7 :
        cid = gcid.getcid(int(sys.argv[1]))
        mid = sys.argv[1]
        action_time = sys.argv[2]
        ho_dist_num = sys.argv[3]
        ho_num = sys.argv[4]
        ct_dist_num = sys.argv[5]
        ct_num = sys.argv[6]
        while True:
            flag = raw_input("Are you when to update message:%s to dist_opens=%s and dist_url_clicks=%s, Please input [y/n]: " % (mid, ho_dist_num, ct_dist_num)) 
            if flag == 'y':
                insert_ho_ct(cid, mid, action_time, int(ho_dist_num), int(ho_num), int(ct_dist_num), int(ct_num))
                print "Done! Update message:%s dist_opens=%s dist_url_clicks=%s" % (mid, ho_dist_num, ct_dist_num) 
                break
            elif flag == 'n':
                print "Nothing is dode !"
                break
            else:
                print "Please input y/n "
    else :
        if sys.argv[1] == '-h':
            print("插入ho、ct数据\nUsage: python %s mid action_time ho_dist_num ho_num ct_dist_num ct_num" % sys.argv[0]);
            sys.exit()
        if sys.argv[1] == '-s':
            mid = sys.argv[2]
            result = src_dist_ho_ct(mid)
            for k, v in result.items():
                print "%20s : %10s" % (k, v)
            sys.exit()
