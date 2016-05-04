#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import sys
import os
import getcid as gcid


def updateToHard(cid, mid, limit_num):
    sql = '''
        update
            msg_%s_%s_h h
        set
            h.return_type_id= 2, h.error_type_id = 204
        where
            h.return_type_id = 1
        limit %s
    '''

    bounce_conn = mdb.get_bounce_conn(cid)
    row_info = mdb.exe_update_sql(bounce_conn, sql % (cid, mid, limit_num), False, True, False, False)
    print row_info

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("修改报表\nUsage: python %s mid limit_num" % sys.argv[0])
    elif len(sys.argv) == 3:
            mid = sys.argv[1]
            limit_num = sys.argv[2]
            cid = gcid.getcid(mid)
            updateToHard(cid, mid, limit_num)
            os.popen('python2.7 /data/wedm/mailcode/console-invoke.py Reporter 10.80.10.204 "direct to report for %s"' % mid)
    else:
        print("修改报表\nUsage: python %s mid limit_num" % sys.argv[0])
