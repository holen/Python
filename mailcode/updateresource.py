#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import sys

#resource_ids="738,739,740"
resource_ids="773,774,775"

def updateresource(src,tag):
    sql = '''
        update resource rc set rc.domains = replace(domains, '%s', '%s') where rc.id in (%s)
    '''

    resource_conn = mdb.get_resource_conn()
    row_info = mdb.exe_update_sql(resource_conn, sql % (src, tag, resource_ids), False, True, False, False)
    print row_info

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("Usage:%s src tag" % sys.argv[0]);
    elif len(sys.argv) == 3:
            src = sys.argv[1]
            tag = sys.argv[2]
            updateresource(src, tag)
    else:
        print("Usage:%s src tag" % sys.argv[0]);


