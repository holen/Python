#-* coding:UTF-8 -*
#!/usr/bin/env python
import mdb as mdb
import sys
import getcid as gcid

def getUserInfo(cid=None, email=None):
    get_user_info = '''
        select 
            u.client_id, u.email_address, u.password, c.client_name, c.branch_id
        from 
            users u,client c
        where 
            u.client_id = c.client_id and 
    '''

    if cid:
        get_user_info += ''' u.client_id = '%s' ''' % cid

    if email :
        get_user_info += '''u.email_address = '%s' ''' % email

    global_conn = mdb.get_global_conn();
    datas = mdb.exe_sql(global_conn, get_user_info, True, True)
    return datas

def getBranchdomain(branch_id):
    sql = '''select bd.domain_name from branch_domain bd where bd.branch_id = %s '''
    
    global_conn = mdb.get_global_conn();
    datas = mdb.exe_sql(global_conn, sql % branch_id, True, True)
    return datas

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-h':
            print("查询客户的用户名密码信息\nUsage: python %s [ client_id ] | [ -m message_id ] | [ -e email_address ]" % sys.argv[0]);
            sys.exit()
        else:
            result = getUserInfo(int(sys.argv[1]))
            branch_id = result[0]['branch_id']
            print "branch_id : %s" % branch_id
            branch_data = getBranchdomain(branch_id)
            for data in branch_data:
                print "Branch_domain: %s" % data['domain_name']
            print "client_id : %s" % result[0]['client_id']
            print "client_name : %s" % result[0]['client_name']
            print "email_address : %s" % result[0]['email_address']
            print "password : %s" % result[0]['password']
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-m':
            cid = gcid.getcid(int(sys.argv[2]))
            result = getUserInfo(int(cid))
            branch_id = result[0]['branch_id']
            print "branch_id : %s" % branch_id
            branch_data = getBranchdomain(branch_id)
            for data in branch_data:
                print "Branch_domain: %s" % data['domain_name']
            print "client_id : %s" % result[0]['client_id']
            print "client_name : %s" % result[0]['client_name']
            print "email_address : %s" % result[0]['email_address']
            print "password : %s" % result[0]['password']
        if sys.argv[1] == '-e':
            email = sys.argv[2]
            result = getUserInfo(email=email)
            branch_id = result[0]['branch_id']
            print "branch_id : %s" % branch_id
            branch_data = getBranchdomain(branch_id)
            for data in branch_data:
                print "Branch_domain: %s" % data['domain_name']
            print "client_id : %s" % result[0]['client_id']
            print "client_name : %s" % result[0]['client_name']
            print "email_address : %s" % result[0]['email_address']
            print "password : %s" % result[0]['password']
    else :
        print("查询客户的用户名密码信息\nUsage: python %s [ client_id ] | [ -m message_id ] | [ -e email_address ]" % sys.argv[0]);
        sys.exit()
