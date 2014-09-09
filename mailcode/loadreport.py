#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
from datetime import datetime, time, timedelta
import sys

def showshortstrategy():
    sql = '''
        select case st.resource_ids 
                when '765' then 'load1' 
                when '747' then 'load2' 
                when '764' then 'load3' 
                when '756' then 'load4' 
                when '777' then 'load5' 
                when '776' then 'load6' 
                end 'load', st.server_ip, st.owner_type, group_concat(st.owner_value) as client_list
        from 
            strategy st 
        where 
            st.domain_key = 'qqdomain' and owner_value <> '' and st.for_test_msg = 0 and st.owner_value not like '-%' 
        group by 
            st.resource_ids, st.owner_type
    '''
    resource_conn = mdb.get_resource_conn()
    datas = mdb.exe_sql(resource_conn, sql, True, True)
    return datas

def sendinfo(start_time, end_time, client_list, group_by=False):
    sql = '''
        select 
            day(ep.start_time) as day, ep.client_id, sum(ep.successful_count) as success, sum(ep.softbounce_count) as soft, sum(ep.unstart_count) as unstart
        from 
            email_package ep 
        where 
            ep.start_time >= '%s' and ep.start_time < '%s' and ep.client_id in (%s) and ep.domain_name = 'qq.com'
    '''
    if(group_by):
        sql += '''group by ep.client_id'''
    carrier_conn = mdb.get_mesher_conn()
    data = mdb.exe_sql(carrier_conn, sql % (start_time, end_time, client_list), True, True)
    return data

def getclients(branch_id):
    sql = '''
        select group_concat(c.client_id) as clients from client c where c.branch_id in (%s)
    '''
    global_conn = mdb.get_global_conn()
    others_clients = mdb.exe_sql(global_conn, sql % (branch_id), True, True)
    return others_clients[0]['clients']

def showreport(start_time, end_time, group_by=False):
    datas = showshortstrategy()
    print "%10s %10s %10s %10s %10s %10s" % ('load', 'day', 'client', 'success', 'soft', 'unstart')
    for data in datas: 
        load = data['load']
        client_list = data['client_list']
        if data['owner_type'] == 'Branch':
            branchs = data['client_list']
            others_clients = getclients(branchs)
            client_list = client_list + ',' + others_clients
        results = sendinfo(start_time, end_time, client_list, group_by)
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
