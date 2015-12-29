#-* coding:UTF-8 -*
#!/usr/bin/env python

import pexpect 
import sys
import mdb as mdb

cmd="/bin/bash /usr/local/application/elink2/service-scripts/controller"

fout = open('/tmp/pexpect.log','wb')

def getActiveService(server):
	sql_str = '''select group_concat(machine_ip) as ips from service s where s.status="active" and s.server_type = "%s" '''
	global_conn = mdb.get_global_conn();
	ips = mdb.exe_sql(global_conn, sql_str % server, True, True)
	return ips[0]['ips'].split(',')

def runcmd(server, ips, commands):
	child=pexpect.spawn(cmd)
	child.expect("START CONTROLLER FINISHED")
	child.sendline("\n")
	
	for ip in ips:
		#service=server.capitalize() +'-'+ ip
		service=server +'-'+ ip
		child.logfile = fout

		child.expect("/>")
		child.sendline("cd %s" % service)

		command_list=commands.split(',')
		for command in command_list:
			child.expect("%s>" % service)
			child.sendline(command)

		child.expect("%s>" % service)
		child.sendline("cd ..")
		
	child.expect("/>")
	child.sendline("exit")

if __name__ == '__main__':
	if sys.argv[1] == '-h':
            print("Usage: python2.7 %s server ip commands" % sys.argv[0]);
            sys.exit()
	server=sys.argv[1]
	ip=sys.argv[2]
	if ip == "all":
		ips=getActiveService(server)
	else:
		ips=[ip]
	commands=sys.argv[3]
	runcmd(server, ips, commands)
