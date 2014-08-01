#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys
from common import mdb as mdb

def get_report_conn(client_id):
    get_reportdb_sql = '''
        select 
            d.db_name
        from 
            client c,db d 
        where 
            c.reporter_db_id=d.db_id and c.client_id = %s
    '''
    # print get_reportdb_sql % client_id

    global_conn = mdb.get_global_conn();
    report_db_name = mdb.exe_sql(global_conn, get_reportdb_sql % (client_id), True, True); 
    return report_db_name[0]['db_name']

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-h':
            print("Usage:%s client_id " % sys.argv[0]);
            sys.exit()
        print get_report_conn(sys.argv[1]) 
    else :
        print("Usage:%s client_id " % sys.argv[0]);
        sys.exit()

