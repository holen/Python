#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import mytexttable as mytt;
import sys

def get_unfinsh_task(message_id):
    select_msg_sql = '''
        select 
            task_id, client_id, object_id, task_status_id, weight, domain_name, schedule_time, claimed_process
        from 
            email_package ep 
        where 
            ep.task_status_id <> 3 and ep.object_id = %s
    '''

    carrier_conn = mdb.get_mesher_conn()
    datas = mdb.exe_sql(carrier_conn, select_msg_sql % (message_id), False, True)
    width = [10] * 6 + [20] + [10] 
    mytt.display(['t_id', 'cid', 'mid', 't_status','weight','domain','s_time','mesher'], datas, width)

def get_task_status(message_id):
    task_status_sql = '''
        select 
            task_id, task_type_id, service_id, client_id, object_id, task_status_id, schedule_time, claimed_process
        from 
            task t
        where 
            t.task_status_id <> 3 and t.object_id = %s
    '''

    global_conn = mdb.get_global_conn()
    datas = mdb.exe_sql(global_conn, task_status_sql % (message_id), False, True)
    width = [10] * 6 + [20] + [10]  
    mytt.display(['t_id', 't_type', 's_id', 'cid', 'mid', 't_status', 's_time', 'claimed'], datas, width)

def getMsgInfo(message_id):
    message_info_sql = ''' 
        select 
            m.client_id,m.message_id,m.subject,m.status_id,m.from_address,m.schedule_time,m.total_count,m.send_count,m.successful_count,m.softbounce_count,m.hardbounce_count,m.unstart_count,m.dist_opens,m.dist_url_clicks 
        from 
            message m 
        where 
            m.message_id = %s
    '''
    global_conn = mdb.get_global_conn()
    datas = mdb.exe_sql(global_conn, message_info_sql % (message_id), True, True)
    print datas[0]['subject']
    #print datas[0].values()
    #width = [10] * 14   
    #mytt.display(['cid', 'mid', 'subject', 's_id', 'f_addree', 's_time', 'totol', 'send', 'succ', 'soft', 'hard', 'unstart', 'open', 'click'], datas, width)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("查询一封邮件还有多少任务在发送\nUsage: python %s message_id " % sys.argv[0]);
        else :
            message_id = sys.argv[1]
            getMsgInfo(message_id)
            get_unfinsh_task(message_id)
            get_task_status(message_id)
    else:
        print("查询一封邮件还有多少任务在发送\nUsage: python %s message_id " % sys.argv[0]);
