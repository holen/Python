#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
from datetime import datetime, time, timedelta
import sys

def showshortstrategy():
    sql = '''
        select case st.resource_ids 
                when '764,776' then '通道1' 
                when '756,797' then '通道2' 
                when '781' then '通道3' 
                when '765,777' then '通道4' 
                when '747' then '通道6' 
                when '780' then '通道7' 
                when '782' then '通道8' 
                when '798' then '通道9' 
                else '其它域'
                end 'load', 
                st.domain_key, st.server_ip, st.owner_type, group_concat(st.owner_value) as client_list
        from 
            strategy st 
        where 
            owner_value <> '' and st.for_test_msg = 0 and st.owner_value not like '-%' 
        group by 
            st.domain_key, st.resource_ids, st.owner_type
    '''
    resource_conn = mdb.get_resource_conn()
    datas = mdb.exe_sql(resource_conn, sql, True, True)
    return datas

def sendinfo(domain, start_time, end_time, client_list, group_by=False):
    sql = '''
        select 
            day(ep.start_time) as day, ep.client_id, sum(ep.successful_count) as success, sum(ep.softbounce_count) as soft, sum(ep.unstart_count) as unstart
        from 
            email_package ep 
        where 
            ep.start_time >= '%s' and ep.start_time < '%s' and ep.client_id in (%s) and ep.domain_name in (%s)
    '''
    if(group_by):
        sql += '''group by ep.client_id'''
    carrier_conn = mdb.get_mesher_conn()
    data = mdb.exe_sql(carrier_conn, sql % (start_time, end_time, client_list, domain), True, True)
    return data

def getclients(branch_id):
    sql = '''
        select group_concat(c.client_id) as clients from client c where c.branch_id in (%s)
    '''
    global_conn = mdb.get_global_conn()
    others_clients = mdb.exe_sql(global_conn, sql % (branch_id), True, True)
    #print others_clients[0]['clients']
    return others_clients[0]['clients']

def showreport(start_time, end_time, group_by=False):
    client_group = "1"
    datas = showshortstrategy()
    print "%10s %10s %10s %10s %10s %10s" % ('load', 'day', 'client', 'success', 'soft', 'unstart')
    for data in datas: 
        load = data['load']
        domain_key = data['domain_key']
        if domain_key == 'qqdomain':
            domain = """'qq.com','vip.qq.com'"""
        elif domain_key == 'netease':
            domain = """'163.com','126.com','vip.163.com','yeah.net'"""
            load = domain_key
        elif domain_key == 'sinadomain':
            domain = """'sina.com','sina.com.cn','sina.cn'"""
            load = domain_key
        else:
            print "wrong domain_key"
            sys.exit()
        client_list = data['client_list']
        if data['owner_type'] == 'Branch':
            branchs = data['client_list']
	    others_clients = getclients(branchs)
	    if others_clients:
	        client_list = client_list + ',' + others_clients
	        client_group = client_group + ',' + client_list

        results = sendinfo(domain, start_time, end_time, client_list, group_by)
        client_group = client_group + ',' + client_list
        for result in results:
            print "%10s %10s %10s %10s %10s %10s" % (load, result['day'], result['client_id'], result['success'], result['soft'], result['unstart'])

if __name__ == '__main__':
    today = datetime.combine(datetime.today(), time(0, 0));
    yestoday = today - timedelta(days=1)
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-h':
            print("查询通道信息\nUsage: python %s [-c] [start_time] " % sys.argv[0]);
            sys.exit()
        elif sys.argv[1] == '-c':
            group_by = True
            showreport(yestoday, today, group_by)
        else:
            start_time = sys.argv[1]
            end_time = datetime.combine(datetime.strptime(start_time, "%Y-%m-%d"), time(0, 0)) + timedelta(days=1)
            showreport(start_time, end_time)
    elif len(sys.argv) == 3 :
        if sys.argv[1] == '-c':
            group_by = True
            start_time = sys.argv[2]
            end_time = datetime.combine(datetime.strptime(start_time, "%Y-%m-%d"), time(0, 0)) + timedelta(days=1)
            showreport(start_time, end_time, group_by)
        else:
            print "The argv 1 is wrong!"
            sys.exit()
    else :
        showreport(yestoday, today)
        sys.exit()
