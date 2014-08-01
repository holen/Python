#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys
import common.mdb as mdb

def selectMessage(mid):
    select_sql = '''
        select 
            count(0)
        from
            email_package ep 
        where 
            ep.task_status_id = 0 and ep.object_id = %s
    '''
    global_conn = mdb.get_global_conn()
    data = mdb.exe_sql(global_conn, select_sql % (mid), False, True)
    print data[0]

def pauseMessage(mid):
    update_sql = '''
        update 
            email_package ep 
        set 
            ep.task_status_id = 5 
        where 
            ep.task_status_id = 0 and ep.object_id = %s
    '''
    carrier_conn = mdb.get_mesher_conn()
    mdb.exe_update_sql(carrier_conn, update_sql % (mid), False, True, False, False)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("暂停邮件\nUsage: python %s mid "% sys.argv[0]);
        else:
            mid = sys.argv[1] 
            selectMessage(mid)
            pauseMessage(mid)
    else:
        print("暂停邮件\nUsage: python %s mid "% sys.argv[0]);
