#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
import sys

def getServerIp(server_id):
    sql = '''
	select 
		ip
	from 
		machine
	where 
		remark = %s
    '''
    
    #print sql % (id)

    try:
        resource_conn = mdb.get_resource_conn()
        loadinfo = mdb.exe_sql(resource_conn, sql % server_id, False, True)
        return loadinfo[0][0]
    except Exception,e:
        print e
        sys.exit()

if __name__ == '__main__':
    server_id = sys.argv[1]
    server_ip = getServerIp(server_id)
    print server_ip
