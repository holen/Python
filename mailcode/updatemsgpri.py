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
    carrier_conn = mdb.get_mesher_conn()
    data = mdb.exe_sql(carrier_conn, select_sql % (mid), False, True)
    return data[0]

def updatemsgpri(mid):
    update_sql = '''
        update 
            email_package ep 
        set 
            ep.priority = 1
        where 
            ep.task_status_id = 0 and ep.object_id = %s
    '''
    try:
        carrier_conn = mdb.get_mesher_conn()
        row_info = mdb.exe_update_sql(carrier_conn, update_sql % (mid), False, True, False, False)
        print row_info
    except Exception,e:
        print e 
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("修改邮件优先级\nUsage: python %s mid "% sys.argv[0]);
        else:
            mid = sys.argv[1] 
            count = selectMessage(mid)
            updatemsgpri(mid)
    else:
        print("修改邮件优先级\nUsage: python %s mid "% sys.argv[0]);
