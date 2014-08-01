#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import mytexttable as mytt;
import sys

def get_task_status(task_id):
    select_msg_sql = '''
        select 
            task_id, task_status_id, domain_name, schedule_time, claimed_process, successful_count, softbounce_count, unstart_count
        from 
            email_package ep 
        where 
            ep.task_id = '%s'
    '''

    carrier_conn = mdb.get_mesher_conn()
    datas = mdb.exe_sql(carrier_conn, select_msg_sql % (task_id), False, True)
    width = [10] * 3 + [20] + [10] * 4
    mytt.display(['t_id','t_status','domain','s_time','mesher','succ','soft','unt'], datas, width)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("查询一个任务包的发送情况\nUsage: python %s task_id " % sys.argv[0]);
        else :
            task_id = sys.argv[1]
            get_task_status(task_id)
    else:
        print("查询一个任务包的发送情况\nUsage: python %s task_id " % sys.argv[0]);
