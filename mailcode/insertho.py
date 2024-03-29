#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys, os
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
file_dir = "/data/git/python/mailcode/hodir"
ho_args_array = []
ct_args_array = []

def read_info(ho_file, ct_file):
	ho_object = open(ho_file, 'rb')
        #ct_args_list.append((unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time))
        #ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time))
	for readline in ho_object:
		ho_args_list = readline.split(',')
		ho_args_array.append(ho_args_list)

	ct_object = open(ct_file, 'rb')
	for readline in ct_object:
		ct_args_list = readline.split(',')
		#return ct_args_list
		#ct_args_array.append(ct_args_list)

	#return ho_args_array, ct_args_array
	return ho_args_array

def insert_to_hoct(cid, ho_file, ct_file):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
	ho_args_array = read_info(ho_file, ct_file)
    	insert_ho_sql = '''INSERT INTO msg_%s_%s_ho (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`, `op_system`, `browser`) values ''' % (cid, mid)
    	insert_ho_sql += '''( %s, %s, 35811, 2, %s, 1, %s, %s, %s, %s, 974586787, 214, %s, %s, %s, NULL, 'Windows 7', 'Unknown' );'''
    	insert_ct_sql = '''INSERT INTO msg_%s_%s_ct (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `url_id`, `url_value`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`) values ''' % (cid, mid) 
    	insert_ct_sql += '''(%s, %s, 35811, 2, %s, 1, %s, %s, %s, %s, %s, %s, 974586787, 214, %s, %s, %s, NULL );'''
	#print insert_ho_sql % (ho_args_list[0], ho_args_list[1], ho_args_list[2], ho_args_list[3], ho_args_list[4], ho_args_list[5], ho_args_list[6], ho_args_list[7], ho_args_list[8], ho_args_list[9])
        reportdb = grid.get_report_conn(cid)
        report_conn = MySQLdb.connect( host=mdb_ip, user=mdb_user, passwd=mdb_pass, db=reportdb ,charset='utf8')
        cursor = report_conn.cursor()
	try:
	    cursor.executemany(insert_ho_sql, ho_args_array)
	    #cursor.executemany(insert_ct_sql, ct_args_list)
	    report_conn.commit()
	except Exception,e:
	    report_conn.rollback()
	    print e
	cursor.close()
	report_conn.close()

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
        ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time))
    for i in range(ho_diff):
        unique_id = 'h6djz8c5'
        email_address = 'ep_10%s@qq.com' % i
        ho_args_list.append((unique_id, mid, cid, email_address, domain_name, action_time))
    ct_args_list = []
    for i in range(int(ct_dist_diff)):
        unique_id = string.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',8)).replace(" ","")
        email_address = 'ep_00%s@qq.com' % i
        ct_args_list.append((unique_id, mid, cid, email_address, domain_name, url_id, url_value, action_time))
    for i in range(int(ct_diff)):
        unique_id = 'h6djz8c5'
        email_address = 'ep_10%s@qq.com' % i
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
	ho_file = "%s/%s_ho.txt" % (file_dir, mid)
	ct_file = "%s/%s_ct.txt" % (file_dir, mid)
	if os.path.isfile(ho_file) and os.path.isfile(ct_file):
		insert_to_hoct(cid, ho_file, ct_file)
		sys.exit()
        action_time = sys.argv[2]
        ho_dist_num = sys.argv[3]
        ho_num = sys.argv[4]
        ct_dist_num = sys.argv[5]
        ct_num = sys.argv[6]
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
