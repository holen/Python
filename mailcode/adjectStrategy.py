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
    insert_load1_sql = '''
        INSERT INTO `strategy` 
            (`server_id`, `server_ip`, `domain_key`, `resource_ids`, `owner_type`, `owner_value`, `for_test_msg`, `switch_type`, `switch_value`, `init_group_size`, `min_group_size`, `last_update_time`, `from_domains`, `remark`) 
        VALUES 
            ('1221377349400', '122.13.77.34', 'qqdomain', '765', 'Client', '%s', 0, 'ByGroup', 12, 30, 1, '2013-03-22 16:28:00', NULL, NULL);
    '''
    insert_load2_sql = '''
        INSERT INTO `strategy` 
            (`server_id`, `server_ip`, `domain_key`, `resource_ids`, `owner_type`, `owner_value`, `for_test_msg`, `switch_type`, `switch_value`, `init_group_size`, `min_group_size`, `last_update_time`, `from_domains`, `remark`) 
        VALUES 
            ('1221377349400', '122.13.77.34', 'qqdomain', '747', 'Client', '%s', 0, 'ByGroup', 12, 30, 1, '2013-03-22 16:28:00', NULL, NULL);
    '''
    insert_load3_sql = '''
        INSERT INTO `strategy` 
            (`server_id`, `server_ip`, `domain_key`, `resource_ids`, `owner_type`, `owner_value`, `for_test_msg`, `switch_type`, `switch_value`, `init_group_size`, `min_group_size`, `last_update_time`, `from_domains`, `remark`) 
        VALUES 
            ('12213771779400', '122.13.77.177', 'qqdomain', '764', 'Client', '%s', 0, 'ByGroup', 12, 28, 1, '2013-03-22 16:28:00', NULL, NULL);
    '''
    insert_load4_sql = '''
        INSERT INTO `strategy` 
            (`server_id`, `server_ip`, `domain_key`, `resource_ids`, `owner_type`, `owner_value`, `for_test_msg`, `switch_type`, `switch_value`, `init_group_size`, `min_group_size`, `last_update_time`, `from_domains`, `remark`) 
        VALUES 
            ('1221377349400', '122.13.77.34', 'qqdomain', '756', 'Client', '%s', 0, 'ByGroup', 12, 30, 1, '2013-03-22 16:28:00', NULL, NULL);
    '''
    sql_dict = { "1": insert_load1_sql, "2": insert_load2_sql, "3": insert_load3_sql, "4": insert_load4_sql }
    sql = sql_dict[load_id]
    try:
        resource_conn = mdb.get_resource_conn()
        row_info = mdb.exe_update_sql(resource_conn, sql % (cid), False, True, False, False)
        print row_info
    except Exception,e:
        print e
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print("调整通道策略Usage: python %s cid load_id" % sys.argv[0]);
    elif len(sys.argv) == 3:
            cid = sys.argv[1]
            load_id = sys.argv[2]
            while True:
                raw_txt = raw_input("Are you when to change client_id: %s to load_%s [y/n]: " % (cid, load_id))
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
