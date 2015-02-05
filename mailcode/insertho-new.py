#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys
import MySQLdb
import getcid as gcid
import getReportdb_id as grid
import common.mdb as mdb
import string, random
import parsexml as parsexml
import argparse

login_info = parsexml.printxmldata("sewcloud")
mdb_user = login_info['user']
mdb_pass = login_info['passwd']
mdb_ip = login_info['ip']

def insert_ho_ct(cid, mid, action_time, ho_dist_num, ho_num, ct_dist_num, ct_num, city):
    domain_name = 'qq.com'
    insert_ho_sql = '''INSERT INTO msg_%s_%s_ho (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`, `op_system`, `browser`) values ''' % (cid, mid)
    insert_ho_sql += '''( %s, %s, 35811, 2, %s, 1, %s, %s, %s, '58.23.3.163', 974586787, %s, %s, %s, %s, NULL, 'Windows 7', 'Unknown' );'''
    insert_ct_sql = '''INSERT INTO msg_%s_%s_ct (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `url_id`, `url_value`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`) values ''' % (cid, mid) 
    insert_ct_sql += '''(%s, %s, 35811, 2, %s, 1, %s, %s, %s, %s, %s, '58.23.3.163', 974586787, %s, %s, %s, %s, NULL );'''

    ip_data = getIpInfo(city)
    place_id = ip_data['place_id']
    country = ip_data['country'].encode('utf8')
    province = ip_data['province'].encode('utf8')
    city = ip_data['city'].encode('utf8')

    reportdb = grid.get_report_conn(cid)
    report_conn = MySQLdb.connect( host=mdb_ip, user=mdb_user, passwd=mdb_pass, db=reportdb ,charset='utf8')
    cursor = report_conn.cursor()
    url = geturl(mid)
    url_id = url['url_id']
    url_value = (url['value']).encode('utf-8')
    src_data = src_dist_ho_ct(mid)
    src_dist_ho = int(src_data['dist_opens'])
    src_ho_num = int(src_data['html_opens'])
    src_dist_ct = int(src_data['dist_url_clicks'])
    src_ct_num = int(src_data['url_clicks'])
    if src_dist_ho >= ho_dist_num:
        ho_dist_diff = 1
    else:
        ho_dist_diff = ho_dist_num - src_dist_ho
    if src_ho_num >= ho_num:
        ho_diff = 1
    else:
        ho_diff = ho_num - src_ho_num
    if src_dist_ct >= ct_dist_num:
        ct_dist_diff = 1
    else:
        ct_dist_diff = ct_dist_num - src_dist_ct
    if src_ct_num >= ct_num:
        ct_diff = 1
    else:
        ct_diff = ct_num - src_ct_num
    ho_args_list = []
    for i in range(ho_dist_diff):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
        email_address = 'ep_00%s@qq.com' % i
        ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time, place_id, country, province, city))
    for i in range(ho_diff):
        unique_id = 'h6djz8c5'
        email_address = 'ep_10%s@qq.com' % i
        ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time, place_id, country, province, city))
    ct_args_list = []
    for i in range(int(ct_dist_diff)):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
        email_address = 'ep_00%s@qq.com' % i
        ct_args_list.append((unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time, place_id, country, province, city))
    for i in range(int(ct_diff)):
        unique_id = 'h6djz8c5'
        email_address = 'ep_10%s@qq.com' % i
        ct_args_list.append((unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time, place_id, country, province, city))
    #print insert_ho_sql % (unique_id, mid, cid, email_address, domain_name, action_time, place_id, country, province, city)
    #print insert_ct_sql % (unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time, place_id, country, province, city)
    #cursor.execute(insert_ho_sql % (unique_id, mid, cid, email_address, domain_name, action_time, place_id, country, province, city))
    #cursor.execute(insert_ct_sql % (unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time, place_id, country, province, city))
    #sys.exit()
    #print ho_args_list
    #print ct_args_list
    try:
        cursor.executemany(insert_ho_sql, ho_args_list)
        cursor.executemany(insert_ct_sql, ct_args_list)
        report_conn.commit()
	print "Done! Update message:%s dist_opens=%s dist_url_clicks=%s" % (mid, ho_dist_num, ct_dist_num) 
    except Exception,e:
        report_conn.rollback()
        print e
    cursor.close()
    report_conn.close()

def getIpInfo(city):
    sql = ''' select place_id, country, province, city from ip_place where city = '%s' '''
    #print city.__class__
    global_conn = mdb.get_global_conn()
    data = mdb.exe_sql(global_conn, sql % (city), True, True)
    return data[0]

def geturl(mid):
    sql = '''
        select url_id, value from track_url t where t.message_id = %s limit 1 
    '''
    try:
    	global_conn = mdb.get_global_conn()
    	data = mdb.exe_sql(global_conn, sql % (mid), True, True)
    	return data[0]
    except Exception,e:
	print "Get message url failed!"

def src_dist_ho_ct(mid):
    sql = '''select message_id, message_name, client_id, end_time, total_count, send_count, successful_count, softbounce_count, hardbounce_count, unstart_count, html_opens, dist_opens, url_clicks, dist_url_clicks from message m where m.message_id = %s'''
    global_conn = mdb.get_global_conn()
    data = mdb.exe_sql(global_conn, sql % (mid), True, True)
    return data[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Insert ho/ct num")
    parser.add_argument("-C", "--cid", action="store", type=int, dest='cid', help="client_id")
    parser.add_argument("-m", "--mid", required=True, action="store", type=int, dest='mid', help="message_id")
    parser.add_argument("-t", "--action_time", action="store", dest='action_time')
    #parser.add_argument("-N", "--ho_dist_num", action="store", type=int, dest='ho_dist_num', help="ho_dist_num")
    parser.add_argument("-N", "--ho_dist_num", action="store", type=int, dest='ho_dist_num')
    parser.add_argument("-n", "--ho_num", action="store", type=int, dest='ho_num')
    parser.add_argument("-D", "--ct_dist_num", action="store", type=int, dest='ct_dist_num')
    parser.add_argument("-d", "--ct_num", action="store", type=int, dest='ct_num')
    parser.add_argument("-c", "--city", action="store", dest='city', help="ho/ct area")
    parser.add_argument("-s", "--show", action="store_true", default=False, help="show message ho/ct info, use with -m")
    args = parser.parse_args()

    cid = args.cid
    mid = args.mid
    action_time = args.action_time
    ho_dist_num = args.ho_dist_num
    ho_num = args.ho_num
    ct_dist_num = args.ct_dist_num
    ct_num = args.ct_num
    #print cid, mid, action_time, ho_dist_num, ho_num, ct_dist_num, ct_num

    if args.city:
	city = args.city
    else:
	city = '厦门市'	

    if args.show:
	result = src_dist_ho_ct(mid)
	for k, v in result.items():
            print "%20s : %10s" % (k, v)
        sys.exit()
    else:
        insert_ho_ct(cid, mid, action_time, int(ho_dist_num), int(ho_num), int(ct_dist_num), int(ct_num), city)
	sys.exit()
