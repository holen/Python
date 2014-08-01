#-* coding:UTF-8 -*
#!/usr/bin/env python

import common.mdb as mdb
import sys

load = { '1' : ['1221377349400','122.13.77.34','765'], 
         '2' : ['1221377349400','122.13.77.34','747'], 
         '3' : ['12213771779400','122.13.77.177','764'], 
         '4' : ['1221377349400','122.13.77.34','756'], 
         '5' : ['22112280219400','221.122.80.21','768,769'],
         '6' : ['22112280219400','221.122.80.21','766']
        } 

def adjectstrategy(cid, load_id):
    sql = '''
        update 
            strategy s 
        set 
            s.server_id = '%s', s.server_ip = '%s', s.resource_ids = '%s'  
        where 
            s.owner_value = '%s'
    '''

    print sql % (load[load_id][0], load[load_id][1], load[load_id][2], cid)
    #resource_conn = mdb.get_resource_conn()
    #mdb.exe_sql(resource_conn, sql % (load[load_id], cid), False, True)

def strategy_exist():
    sql = '''
        select 
    '''

def insertnewstg():
    sql = '''
        INSERT INTO 
            `strategy`(`server_id`, `server_ip`, `domain_key`, `resource_ids`, `owner_type`, `owner_value`, `for_test_msg`, `switch_type`, `switch_value`, `init_group_size`, `min_group_size`, `last_update_time`, `from_domains`, `remark`) 
        VALUES 
            ('%s', '%s', 'qqdomain', '%s', 'Client', '%s', 0, 'ByGroup', 12, 30, 1, '2013-03-22 16:28:00', NULL, NULL)
    '''

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("Usage:%s cid load_id" % sys.argv[0]);
    elif len(sys.argv) == 3:
            cid = sys.argv[1]
            load_id = sys.argv[2]
            adjectstrategy(cid, load_id)
    else:
        print("Usage:%s cid load_id" % sys.argv[0]);
