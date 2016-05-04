#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import sys
import getcid as gcid

def updateBounce(cid, mid, last_rt_id, limit_num):
    sql = '''
        update 
            msg_%s_%s_u u 
        set 
            u.last_rt_id = 1, u.last_et_id = -1 
        where 
            u.last_rt_id = %s
        limit %s
    '''

    bounce_conn = mdb.get_bounce_conn(cid)
    row_info = mdb.exe_update_sql(bounce_conn, sql % (cid, mid, last_rt_id, limit_num), False, True, False, False)
    print row_info

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("修改报表\nUsage: python %s mid last_rt_id limit_num "% sys.argv[0]);
    elif len(sys.argv) == 4:
            mid = sys.argv[1]
            last_rt_id = sys.argv[2]
            limit_num = sys.argv[3]
            cid = gcid.getcid(mid)
	    updateBounce(cid, mid, last_rt_id, limit_num)
    else:
        print("修改报表\nUsage: python %s mid last_rt_id limit_num "% sys.argv[0]);
