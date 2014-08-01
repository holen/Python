#-* coding:UTF-8 -*
#!/usr/bin/env python

import clowqmdb as cmdb
import common.mdb as mdb
from datetime import datetime, time, timedelta
import texttable as tt;
import sys

result_data = []

def display(header, data, cols=None):
    if not cols:
        cols = ['c'] * len(header);        
    display_schedule_tbl = tt.Texttable();
    display_schedule_tbl.set_cols_width([10,10,20,10,10,10,10,10]);
    display_schedule_tbl.set_cols_align(cols); display_data = [header];
    display_data.extend(data);
    display_schedule_tbl.add_rows(display_data); 
    display = display_schedule_tbl.draw();  
    print display
    result_data.append(display)

def get_msg_report(start=None):
    today = datetime.combine(datetime.today(), time(0, 0));
    today_9 = datetime.combine(datetime.today(), time(9, 0));
    yesterday = today - timedelta(hours=24);
    select_msg_sql = '''
        select 
            m.client_id, m.message_id, m.schedule_time, m.status_id, m.send_count, m.successful_count, m.softbounce_count, m.unstart_count
        from 
            message m 
        where 
            m.schedule_time >= '%s' and m.schedule_time <= '%s' 
    '''

    if(not start):
        start = yesterday;
        end = today_9
    else:
        end = datetime.strptime(start, '%Y-%m-%d').date() + timedelta(hours=24)

    sw_global_conn = mdb.get_global_conn()
    sw_datas = mdb.exe_sql(sw_global_conn, select_msg_sql % (start, end), False, True)

    #c_global_conn = cmdb.get_global_conn()
    #c_datas = mdb.exe_sql(c_global_conn, select_msg_sql % (start, end), False, True)

    display(['cid','mid', 'stime', 'status','send','succ','soft','unstart'], sw_datas)
    #display(['cid','mid', 'stime', 'status','send','succ','soft','unstart'], c_datas)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("查看报表\nUsage: python %s [start_time] " % sys.argv[0]);
        else :
            start = sys.argv[1]
            get_msg_report(start)
    else:
        get_msg_report()
