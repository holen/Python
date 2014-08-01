#-* coding:UTF-8 -*
#!/usr/bin/env python
import mdb as mdb
import sys
import getcid as gcid

def getUserInfo(cid=None, email=None):
    get_user_info = '''
        select 
            u.client_id, u.email_address, u.password, c.client_name
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

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-h':
            print("查询客户的用户名密码信息\nUsage: python %s [ client_id ] | [ -m message_id ] | [ -e email_address ]" % sys.argv[0]);
            sys.exit()
        else:
            result = getUserInfo(int(sys.argv[1]))
            print "client_id : %s" % result[0]['client_id']
            print "client_name : %s" % result[0]['client_name']
            print "email_address : %s" % result[0]['email_address']
            print "password : %s" % result[0]['password']
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-m':
            cid = gcid.getcid(int(sys.argv[2]))
            result = getUserInfo(int(cid))
            print "client_id : %s" % result[0]['client_id']
            print "client_name : %s" % result[0]['client_name']
            print "email_address : %s" % result[0]['email_address']
            print "password : %s" % result[0]['password']
        if sys.argv[1] == '-e':
            email = sys.argv[2]
            result = getUserInfo(email=email)
            print "client_id : %s" % result[0]['client_id']
            print "client_name : %s" % result[0]['client_name']
            print "email_address : %s" % result[0]['email_address']
            print "password : %s" % result[0]['password']
    else :
        print("查询客户的用户名密码信息\nUsage: python %s [ client_id ] | [ -m message_id ] | [ -e email_address ]" % sys.argv[0]);
        sys.exit()

