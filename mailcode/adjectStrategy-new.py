#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
import sys, argparse
from getloadstr import getLoadInfo
from getserverip import getServerIp
from showresource import getresource

def deloldstg(domainkey, owner_value):
    sql = " delete from strategy where domain_key = '%s' and owner_value = %s " 
    try:
        resource_conn = mdb.get_resource_conn()
        #print sql % (domainkey, owner_value)
        row_info = mdb.exe_update_sql(resource_conn, sql % (domainkey, owner_value), False, True, False, False)
        print row_info
    except Exception,e:
        print e
        sys.exit()

def selectstg(domainkey, owner_value):
    sql = " select * from strategy s where s.domain_key = '%s' and s.owner_value = %s "
    try:
        resource_conn = mdb.get_resource_conn()
        #print sql % (domainkey, owner_value)
        result = mdb.exe_sql(resource_conn, sql % (domainkey, owner_value), False, True)
        return result
    except Exception,e:
        print e
        sys.exit()

def insertnewstg(server_id, server_ip, domainkey, resource_ids, owner_type, owner_value, for_test_msg, switch_type, switch_value, init_group_size, min_group_size):
    insert_load_sql = '''
        INSERT INTO `strategy` 
            (`server_id`, `server_ip`, `domain_key`, `resource_ids`, `owner_type`, `owner_value`, `for_test_msg`, `switch_type`, `switch_value`, `init_group_size`, `min_group_size`, `last_update_time`, `from_domains`, `remark`) 
        VALUES 
            ('%s', '%s', '%s', '%s', '%s', %s, %s, '%s', %s, %s, %s, '2015-03-22 16:28:00', NULL, NULL);
    '''
    try:
        resource_conn = mdb.get_resource_conn()
        #print insert_load_sql % (server_id, server_ip, domainkey, resource_ids, owner_type, owner_value, for_test_msg, switch_type, switch_value, init_group_size, min_group_size)
        row_info = mdb.exe_update_sql(resource_conn, insert_load_sql % (server_id, server_ip, domainkey, resource_ids, owner_type, owner_value, for_test_msg, switch_type, switch_value, init_group_size, min_group_size), False, True, False, False)
        print row_info
    except Exception,e:
        print e
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="配置通道\n\nExample:\n    QQ:   python %(prog)s -d qqdomain -c 80008 -l 2\n    163:  python %(prog)s -d netease -c 80008 -r 799\n    sina: python %(prog)s -d sinadomain -c 8008 -r 799")
    parser.add_argument("-d", "--domainkey", action="store", dest='domainkey', default='qqdomain', 
                            help="domainkey: qqdomain, netease, sinadomain, elink.other, default")
    parser.add_argument("-D", "--delete", action="store_true", help="Delete strategy!")
    parser.add_argument("-c", "--owner_value", required=True, type=int, action="store", dest='owner_value', 
                            help="client id")
    parser.add_argument("-l", "--load_id", action="store", dest='load_id', help="load_id just for QQ domain")
    parser.add_argument("-r", "--resource_ids", action="store", dest='resource_ids', help="resource_id for strategy")
    parser.add_argument("-t", "--for_test_msg", action="store", type=int, dest='for_test_msg', default=0, 
                            help="test msg, 0 or 1 ")
    parser.add_argument("-o", "--owner_type", action="store", dest="owner_type", default="Client", 
                            help="owner_type: Message, Project, Division, Client, Branch, Common")
    args = parser.parse_args()
    
    min_group_size = 1
    owner_value = args.owner_value
    domainkey = args.domainkey
    
    if domainkey == "qqdomain":
        switch_type = "ByGroup"
        switch_value = 12
    else:
        switch_type = "ByTime"
        switch_value = 720

    if args.delete :
        deloldstg(domainkey, owner_value)
        print "Done! delete old strategy on client_id: %s " % owner_value
        sys.exit()

    owner_type = args.owner_type
    for_test_msg = args.for_test_msg

    flag = selectstg(domainkey, owner_value)
    if(flag):
        deloldstg(domainkey, owner_value)
    
    if args.resource_ids:
        rids = args.resource_ids
        rinfos = getresource(rids)
        for rinfo in rinfos:
            server_id = rinfo['server_id']
            server_ip = getServerIp(rinfo['server_id'])
            resource_ids = rinfo['rids']
            init_group_size = rinfo['count']
            try:
                resource_conn = mdb.get_resource_conn()
                insertnewstg(server_id, server_ip, domainkey, resource_ids, owner_type, owner_value, for_test_msg, 
                            switch_type, switch_value, init_group_size, min_group_size)
                print "Done! Add a new strategy at client_id: %s on %s " % (owner_value, domainkey)
            except Exception,e:
                print e
                sys.exit()
    elif args.load_id:
        load_id = args.load_id
        load_array = getLoadInfo(load_id)
        for load_list in load_array:
            try:
                resource_conn = mdb.get_resource_conn()
                server_id = load_list['server_id']
                server_ip = getServerIp(load_list['server_id'])
                resource_ids = load_list['rids']
                init_group_size = load_list['count']
                insertnewstg(server_id, server_ip, domainkey, resource_ids, owner_type, owner_value, for_test_msg, 
                                switch_type, switch_value, init_group_size, min_group_size)
                print "Done! Add a new strategy at client_id: %s on %s " % (owner_value, domainkey)
            except Exception,e:
                print e
                sys.exit()
    else:
        print "No enough argument, please get resource_ids or load_id !"
        sys.exit()
