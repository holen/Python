# encoding=utf8  
import mdb as mdb
import csv
import os
import shutil
from datetime import datetime, time, timedelta, date
import sys
reload(sys)
sys.setdefaultencoding('gb2312')

def get_group_mail(group_id):

    get_group_sql = '''
        select 
            mg.group_name,m.client_id,group_concat(m.message_id) as messages 
        from 
            message m, message_group mg 
        where 
            mg.group_id = m.group_id and m.group_id = %s
        group by 
            m.group_id;
    '''
    global_conn = mdb.get_global_conn();
    datas = mdb.exe_sql(global_conn, get_group_sql % (group_id), True, True);
    return datas

def export(flag,datas):
    the_file='%s.csv' % (flag)
    csvfile = file('%s' % (the_file), 'ab')
    writer = csv.writer(csvfile)
    # Bool = os.path.isfile(the_file)
    # if flag == "sucess" and not Bool:
    #     writer.writerow(['message_id', 'email'])
    # if flag == "soft" and not Bool:
    #     writer.writerow(['message_id', 'email'])
    # if flag == "open" and not Bool:
    #     writer.writerow(['message_id', 'email', 'ip', 'country', 'province', 'city'])
    # if flag == "dict" and not Bool:
    #     writer.writerow(['message_id', 'url', 'email', 'ip', 'country', 'province', 'city'])
    writer.writerows(datas)
    csvfile.close();

def get_data(group_id):
    the_date = date.today()

    print '%s is begin!' % (group_id)
    sum=0

    get_sucess_sql = '''select u.message_id,u.email from msg_%s_%s_u u where u.last_rt_id = 1;'''
    get_soft_sql   = '''select u.message_id,u.email from msg_%s_%s_u u where u.last_rt_id = 2;'''
    get_open_sql   = '''select ho.message_id,ho.email_address,ho.ip,ho.country,ho.province,ho.city from msg_%s_%s_ho ho;'''
    get_dict_sql   = '''select ct.message_id,ct.url_value,ct.email_address,ct.ip,ct.country,ct.province,ct.city from msg_%s_%s_ct ct;'''

    report     = get_group_mail(group_id);
    group_name = report[0]["group_name"]
    client_id  = report[0]["client_id"]
    messages   = report[0]["messages"].split(',')
    the_dir    = "E:\\groupdata\\%s.%s" % (group_id,group_name);
    if os.path.exists(the_dir):
        os.rename(the_dir,'%s.%s' % (the_dir,the_date))
    os.mkdir('%s' % (the_dir))
    os.chdir('%s' % (the_dir))
    for message_id in messages:

        bounce_conn = mdb.get_bounce_conn(client_id);
        try:
            sucess_datas = mdb.exe_sql(bounce_conn, get_sucess_sql % (client_id,message_id), False, False);
        except Exception,e:
            continue
        export('sucess',sucess_datas)
        sum+=1
        print '%s sucess done!' % (message_id)
        try:
            soft_datas = mdb.exe_sql(bounce_conn, get_soft_sql % (client_id,message_id), False, False);
        except Exception,e:
            continue
        export('soft',soft_datas)
        print '%s soft done!' % (message_id)
        mdb.close_conn(bounce_conn)

        report_conn = mdb.get_report_conn(client_id);
        try:
            open_datas = mdb.exe_sql(report_conn, get_open_sql % (client_id,message_id), False, False);
        except Exception,e:
            continue
        export('open',open_datas)
        print '%s open done!' % (message_id)
        try:
            dict_datas = mdb.exe_sql(report_conn, get_dict_sql % (client_id,message_id), False, False);
        except Exception,e:
            continue
        export('dict',dict_datas)
        print '%s dict done!' % (message_id)
        mdb.close_conn(report_conn)
    else:
        print '%s is end!' % (group_id)

    if sum == 0:
        os.chdir("E:\\groupdata")
        shutil.rmtree(the_dir)

if __name__ == '__main__':  
    for i in range(433,450):
        get_data(i);