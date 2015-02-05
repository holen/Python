#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
import sys
from getloadstr import getLoadInfo
from getserverip import getServerIp

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

def deloldstg(cid):
    sql = " delete from strategy where domain_key = 'qqdomain' and owner_value = %s " 
    try:
        resource_conn = mdb.get_resource_conn()
        row_info = mdb.exe_update_sql(resource_conn, sql % (cid), False, True, False, False)
        print row_info
    except Exception,e:
        print e
        sys.exit()

def selectstg(cid):
    sql = " select * from strategy s where s.domain_key = 'qqdomain' and s.owner_value = %s "
    try:
        resource_conn = mdb.get_resource_conn()
        result = mdb.exe_sql(resource_conn, sql % (cid), False, True)
        return result
    except Exception,e:
        print e
        sys.exit()

def insertnewstg(cid, load_id):
    insert_load_sql = '''
        INSERT INTO `strategy` 
            (`server_id`, `server_ip`, `domain_key`, `resource_ids`, `owner_type`, `owner_value`, `for_test_msg`, `switch_type`, `switch_value`, `init_group_size`, `min_group_size`, `last_update_time`, `from_domains`, `remark`) 
        VALUES 
            ('%s', '%s', 'qqdomain', '%s', '%s', '%s', 0, 'ByGroup', 12, %s, 1, '2013-03-22 16:28:00', NULL, NULL);
    '''
    if int(cid) < 3000:
        owner_type = 'Branch'
    else:
        owner_type = 'Client'
    #load_array = load[load_id]
    load_array = getLoadInfo(load_id)
    #print load_array
    #print insert_load_sql % (load_list[0], load_list[1], load_list[2], owner_type, cid, load_list[3]) 
    for load_list in load_array:
        try:
            #print load_list
            resource_conn = mdb.get_resource_conn()
            load_list['server_ip'] = getServerIp(load_list['server_id'])
            #print insert_load_sql % (load_list['server_id'], load_list['server_ip'], load_list['rids'], owner_type, cid, load_list['count'])
            row_info = mdb.exe_update_sql(resource_conn, insert_load_sql % (load_list['server_id'], load_list['server_ip'], load_list['rids'], owner_type, cid, load_list['count']), False, True, False, False)
            print row_info
        except Exception,e:
            print e
            sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("调整通道策略Usage: python %s [-d] cid load_id" % sys.argv[0]);
    elif len(sys.argv) == 3:
            if sys.argv[1] == "-d":
                cid = sys.argv[2]
                deloldstg(cid)
                print "Done! delete old strategy on client_id: %s " % cid
            else:
                cid = sys.argv[1]
                load_id = sys.argv[2]
                while True:
                    raw_txt = raw_input("Do you when to change client_id: %s to load_%s [y/n]: " % (cid, load_id))
                    if raw_txt == 'y':
                        flag = selectstg(cid)
                        if(flag):
                            deloldstg(cid)
                            insertnewstg(cid, load_id)
                            print "Done! delete old strategy on client_id: %s and add new strategy to load_%s" % (cid, load_id)
                        else:
                            insertnewstg(cid, load_id)
                            print "Done! Add a new strategy on client_id: %s on load_%s " % (cid, load_id)
                        break
                    elif raw_txt == 'n':
                        print "Nothing is dode !"
                        break
                    else:
                        print "Please input y/n "
    else:
        print("调整通道策略Usage: python %s cid load_id" % sys.argv[0]);
