#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import mytexttable as nt
import sys
from getloadstr import showLoadInfo

def getload():
    load = {}
    loadinfos = showLoadInfo()
    #print loadinfos
    for loadinfo in loadinfos:
        load[loadinfo['rids']] = loadinfo['domains'].split(".")[0]
    return load

def showstrategy():
    sql = '''
        select 
            st.domain_key, st.server_id,st.domain_key,st.resource_ids,st.owner_type,st.owner_value,st.for_test_msg
        from 
            strategy st 
        where 
            st.owner_value not like '-%' and owner_type <> 'Common'
        order by 
            st.domain_key
    '''

    resource_conn = mdb.get_resource_conn()
    datas = list(mdb.exe_sql(resource_conn, sql, True, True))
    return datas

def showshortstrategy():
    sql = '''
        select 
            st.domain_key, st.resource_ids, st.server_ip, st.owner_type, group_concat(st.owner_value) as owner_values
        from 
            strategy st 
        where 
            owner_value <> '' and st.for_test_msg = 0 and st.owner_value not like '-%' 
        group by 
            st.domain_key, st.resource_ids, st.owner_type
    '''
    resource_conn = mdb.get_resource_conn()
    datas = list(mdb.exe_sql(resource_conn, sql, True, True))
    return datas

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-r':
            datas = showshortstrategy()
            load = getload()
            print '''\n     load   resource_ids    server_ip   owner_type  owner_values \n'''
            for data in datas:
                if data['domain_key'] == 'qqdomain':
                    load_info = load[data['resource_ids']]
                else:
                    load_info = data['domain_key']
                print '%10s %10s %15s %10s %15s \n' % (load_info, data['resource_ids'], data['server_ip'], data['owner_type'], data['owner_values'])
        elif sys.argv[1] == '-h':
            print("查询通道信息\nUsage: python %s [-r] " % sys.argv[0]);
            sys.exit()
    else :
        datas = showstrategy()
        load = getload()
        print '''\n     load    server_id       domain_key    rids   owner_type  owner_values from_test_msg\n'''
        for data in datas:
            if data['domain_key'] == 'qqdomain':
                load_info = load[data['resource_ids']]
            else:
                load_info = data['domain_key']
            print '%10s %15s %10s %10s %10s %10s %10s \n' % (load_info, data['server_id'], data['domain_key'], data['resource_ids'], data['owner_type'], data['owner_value'], data['for_test_msg'])
        sys.exit()
