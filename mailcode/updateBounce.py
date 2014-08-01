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
    mdb.exe_update_sql(bounce_conn, sql % (cid, mid, last_rt_id, limit_num), False, True, False, False)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("修改报表\nUsage: python %s mid last_rt_id limit_num "% sys.argv[0]);
    elif len(sys.argv) == 4:
            mid = sys.argv[1]
            last_rt_id = sys.argv[2]
            limit_num = sys.argv[3]
            cid = gcid.getcid(mid)
            while True:
                flag = raw_input("There are affect %s rows on messages:%s and the last_rt_id=%s, are you when to continue [y/n]: " % (limit_num, mid, last_rt_id))
                if flag == 'y':
                    updateBounce(cid, mid, last_rt_id, limit_num)
                    print "Done! Update message:%s last_rt_id=%s to 1 limit %s" % (mid, last_rt_id, limit_num)
                    break
                elif flag == 'n':
                    print "Nothing is dode !"
                    break
                else:
                    print "Please input y/n " 
    else:
        print("修改报表\nUsage: python %s mid last_rt_id limit_num "% sys.argv[0]);
