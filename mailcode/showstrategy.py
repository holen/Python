#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import mytexttable as nt
import sys

def showstrategy():
    sql = '''
        select 
            st.server_id,st.domain_key,st.resource_ids,st.owner_type,st.owner_value,st.for_test_msg,
            case st.resource_ids 
                when '765' then '通道1' 
                when '747' then '通道2' 
                when '764' then '通道3' 
                when '756' then '通道4' 
                when '768,769' then '通道5' 
                when '766' then '通道6' 
                else '其他通道' end 'load'
        from 
            strategy st 
        where 
            st.domain_key = 'qqdomain' and st.owner_value not like '-%' 
        order by 
            st.resource_ids 
    '''

    resource_conn = mdb.get_resource_conn()
    data = list(mdb.exe_sql(resource_conn, sql, False, True))
    head = ['server_id', 'domain', 'rid', 'o_type', 'o_value', 'isTest', '通道']
    width = [11] * 7
    nt.display(head,data,width)

def showshortstrategy():
    sql = '''
        select case st.resource_ids 
                when '765' then 'load1' 
                when '747' then 'load2' 
                when '764' then 'load3' 
                when '756' then 'load4' 
                when '768,769' then 'load5' 
                when '766' then 'load6' 
                end 'load', st.server_ip, st.owner_type, group_concat(st.owner_value) 
        from 
            strategy st 
        where 
            st.domain_key = 'qqdomain' and owner_value <> '' and st.for_test_msg = 0 and st.owner_value not like '-%' 
        group by 
            st.resource_ids, st.owner_type
    '''
    resource_conn = mdb.get_resource_conn()
    data = list(mdb.exe_sql(resource_conn, sql, False, True))
    head = ['load', 'server_ip', 'owner_type', 'clients']
    width = [10] + [20] + [10] + [50]
    nt.display(head,data,width)

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-r':
            showshortstrategy()
        elif sys.argv[1] == '-h':
            print("查询通道信息\nUsage: python %s [-r] " % sys.argv[0]);
            sys.exit()
    else :
        showstrategy()
        sys.exit()
