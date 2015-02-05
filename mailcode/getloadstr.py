#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
import sys

#load = { '1' : [ ['1221377349400', '122.13.77.34', '765,777', '46'], 
#		 ['12213771779400','122.13.77.177','764,776', '44'] 
#		], 
#         '2' : [ ['1221377349400', '122.13.77.34', '747,756', '60'], 
#         	 ['12213752179400', '122.13.75.217', '780,781,782', '47'] 
#		], 
#         '3' : [ ['1221377349400', '122.13.77.34', '797,798', '32'] 
#		],
#         '4' : [ ['1221377349400', '122.13.77.34', '794,795', '32'] 
#		]
#        } 

def getLoadInfo(id):
    sql = '''
	select 
		r.domains,group_concat(r.id) as rids, r.server_id, sum(to_index+1) - sum(from_index) as count
	from 
		resource r 
	where 
		r.id <> 796 and r.domains = "load%s.com"
	group by 
		r.domains,r.server_id 
	order by r.domains 
    '''
    
    #print sql % (id)

    try:
        resource_conn = mdb.get_resource_conn()
        loadinfo = mdb.exe_sql(resource_conn, sql % id, True, True)
        return loadinfo
    except Exception,e:
        print e
        sys.exit()

def showLoadInfo():
    sql = '''
	select 
		r.domains,group_concat(r.id) as rids
	from 
		resource r 
	where 
		r.id <> 796 and r.domains like 'load%%'
	group by 
		r.domains,r.server_id 
	order by r.domains 
    '''
    
    try:
        resource_conn = mdb.get_resource_conn()
        loadinfo = mdb.exe_sql(resource_conn, sql, True, True)
        return loadinfo
    except Exception,e:
        print e
        sys.exit()

if __name__ == '__main__':
    id = int(sys.argv[1])
    loadinfos = getLoadInfo(id)
    for loadinfo in loadinfos:
        print loadinfo
