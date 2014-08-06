#-* coding:UTF-8 -*
#!/usr/bin/env python
import common.mdb as mdb
import sys

def getUserInfo(user_name):
    get_user_info = '''
       select a.user_name, a.password from admin_user a where a.user_name = '%s'
    '''

    try:
        admin_conn = mdb.get_admin_conn();
        datas = mdb.exe_sql(admin_conn, get_user_info % user_name, True, True)
        return datas
    except Exception,e:
        print e
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        if sys.argv[1] == '-h':
            print("查询管理员用户名密码信息\nUsage: python %s user_name " % sys.argv[0]);
            sys.exit()
        else:
            result = getUserInfo(sys.argv[1])
            if(result):
                print "user_name : %s" % result[0]['user_name']
                print "password : %s" % result[0]['password']
            else:
                print "The user_name: %s is no exist!" % sys.argv[1]
    else:
        print("查询管理员用户名密码信息\nUsage: python %s user_name " % sys.argv[0]);
