#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
import sys
import argparse

def getresource(rids):
    sql = '''
	select 
		r.domains,group_concat(r.id) as rids, r.server_id, sum(to_index+1) - sum(from_index) as count
	from 
		resource r 
	where 
		r.id in (%s)
	group by 
		r.server_id, r.domains 
	order by 
        r.server_id
    '''
    
    try:
        resource_conn = mdb.get_resource_conn()
        loadinfo = mdb.exe_sql(resource_conn, sql % rids, True, True)
        return loadinfo
    except Exception,e:
        print e
        sys.exit()

def showresource():
    sql = '''
	select 
		r.domains,group_concat(r.id) as rids, r.server_id, sum(to_index+1) - sum(from_index) as count
	from 
		resource r 
	group by 
		r.domains,r.server_id 
	order by 
        r.domains 
    '''
    
    try:
        resource_conn = mdb.get_resource_conn()
        loadinfo = mdb.exe_sql(resource_conn, sql, True, True)
        return loadinfo
    except Exception,e:
        print e
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="show resources info")
    parser.add_argument("-r", "--rids", action="store", dest="rids", help="resource_ids")
    args = parser.parse_args()
    if args.rids:
        rids = args.rids
        resourceinfos = getresource(rids)
        for resourceinfo in resourceinfos:
            print resourceinfo
    else:
        datas = showresource()
        for data in datas:
            print data
