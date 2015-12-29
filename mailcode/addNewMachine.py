#-* coding:UTF-8 -*
#!/usr/bin/env python

import subprocess
import mdb as mdb
import sys

service_dict={
	'loader': '9310',
	'deploy': '9320',
	'reportRefresher': '9330',
	'reporter': '9340',
	'harvester': '9350',
	'miniharvester': '9370',
	'mesher': '9400',
	'uiexport': '9410',
	'Bounceserver': '9420'
}

def insertMachine(ip, server_type):
	sql_machine = '''
		INSERT INTO `machine` (`ip`, `ssh_port`, `machine_group`, `passwd`, `remark`) VALUES 
	("%s", 22, "%s", 'WcLPHVvGyY327E8fRSlGRV14MBuM0skG0tN/mPpmxvX/L+YyTlSPzWGq/BIhtmyTvPAwqX4ewszLdySr1uqN6q3otreTNBja0pcB2FREdFjzcX31KjuX9u4F6UNUjZHk+bQ7w4fUDQ5VEhmVASsxxtIk/xouRFLPL2LkFagi4OI=', now());
	'''
	sql_service = '''
	INSERT INTO `service` (`server_id`,`machine_ip`,`server_type`,`server_port`,`status`,`pressure`,`launch_on`,`shutdown_on`,`refresh_on`,`doSuspend`,`doStop`) VALUES 
	("%s", "%s", "%s", %s, 'down', 0, now(), now(), now(), 1, 1);
	'''
	
	port=service_dict[server_type]
	server_id=ip.replace('.','')+port

	try:
		global_conn = mdb.get_global_conn();
		mdb.exe_insert_sql(global_conn, sql_machine % (ip, server_type), False, False)
		mdb.exe_insert_sql(global_conn, sql_service % (server_id, ip, server_type, port), False, True)
	except Exception,e:
		print "Insert machine info failed!"
		sys.exit()

def sshcmd(ip):
	subprocess.call('ssh %s "yum install -y mysql nfs-utils glibc.i686"' % ip, shell=True)
	subprocess.call('ssh %s "echo -e "117.25.143.17 db.sewcloud.ltd\n117.25.143.17 trigger.epcare.com.cn" >> /etc/hosts"' % ip, shell=True)
	subprocess.call('ssh %s "mkdir /usr/local/application"' % ip, shell=True)
	subprocess.call('ssh %s "mount -t nfs 117.25.143.17:/data/wedm/ /usr/local/application/"' % ip, shell=True)
		
if __name__ == '__main__':
	server_type=sys.argv[1]
	ip=sys.argv[2]
	insertMachine(ip, server_type)
	sshcmd(ip)

