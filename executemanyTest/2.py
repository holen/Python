#-* coding:UTF-8 -*
#!/usr/bin/env python

import sys
import MySQLdb
 
# 连接数据库　
try:
    conn = MySQLdb.connect(host='10.10.11.202',user='epcare',passwd='sewcloud@mysql@2014',db='test',charset='utf8')
except Exception, e:
    print e
    sys.exit()
 
# 获取cursor对象来进行操作
 
cursor = conn.cursor()
# 创建表
#sql = "create table if not exists test2(name varchar(128) primary key, age int(4), num int(4))"
#cursor.execute(sql)
# 插入数据
#sql = "insert into test2(name, age, num) values ('%s', %d, %d)" % ("zhaowei", 23, 1)
#try:
#    cursor.execute(sql)
#except Exception, e:
#    print e
 
#sql = "insert into test2(name, age, num) values ('%s', %d, %d)" % ("张三", 21, 2)
#try:
#    cursor.execute(sql)
#except Exception, e:
#    print e
# 插入多条
 
#sql = "insert into msg_1_29_ho (name, age, num) values (%s, %s, 3)"
sql = '''INSERT INTO msg_1_29_ho (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`, `op_system`, `browser`) values ( 'ou7qdygz', %s, 35811, 2, %s, 1, %s, %s, %s, '58.23.3.163', 974586787, 214, '中国', '福建', '厦门市', NULL, 'Windows 7', 'Unknown' );'''
sql = "INSERT INTO msg_%s_%s_ho (`unique_id`, `message_id`, `list_id`, `subscriber_id`, `client_id`, `user_id`, `email_address`, `domain_name`, `action_time`, `ip`, `ip_long`, `place_id`, `country`, `province`, `city`, `point`, `op_system`, `browser`) values " % (1, 29)
sql += "( 'ou7qdygz', %s, 35811, 2, %s, 1, %s, %s, %s, '58.23.3.163', 974586787, 214, '中国', '福建', '厦门市', NULL, 'Windows 7', 'Unknown' );"
#val = (("李四", 24), ("王五", 25), ("洪六", 26))
#val = [("李四", 24), ("王五", 25), ("洪六", 26)]
val = [(29, 1, 'ep_0001@qq.com', 'qq.com', '2014-07-30 10:32:04'), (29, 1, 'ep_0001@qq.com', 'qq.com', '2014-07-30 10:32:04')]
print val
try:
    cursor.executemany(sql, val)
except Exception, e:
    print e
 
#查询出数据
sql = "select * from msg_1_29_ho"
cursor.execute(sql)
alldata = cursor.fetchall()
# 如果有数据返回，就循环输出, alldata是有个二维的列表
if alldata:
    for rec in alldata:
        print rec
 
 
cursor.close()
conn.close()
