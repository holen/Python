#!/usr/bin/python
#coding=UTF-8

import commands;
import sys;
import time;
import datetime
import os;

class UpgradeUtils(object):
    
    ssh_port = {
        "10.10.12.11"   : "922",
        "10.10.13.10"   : "922",
    }
    
    servers = {
        "loader" : {
            "name" : "loader",
            "port" : "9310",
            "locations" : "10.10.10.141",
            "doSuspend" : True,
        },
        
        "deployer" : {
            "name" : "deployer",
            "port" : "9320",
            "locations" : "10.10.10.141",
            "doSuspend" : True,
        },
        
        "reporter" : {
            "name" : "reporter",
            "port" : "9340",
            "locations" : "10.10.10.141",
            "doSuspend" : True
        },
        
        "exporter" : {
            "name" : "exporter",
            "port" : "9390",
            "locations" : "10.10.10.141",
            "doSuspend" : True
        },
        
        "uiexporter" : {
            "name" : "uiexporter",
            "port" : "9410",
            "locations" : "10.10.10.141",
            "doSuspend" : True
        },
        
        "packer" : {
            "name" : "packer",
            "port" : "9360",
            "locations" : "10.10.10.141",
            "doSuspend" : True
        },
        
        "miniharvester" : {
            "name" : "miniharvester",
            "port" : "9370",
            "locations" : "10.10.10.141",
            "doSuspend" : True
        },
        
        "harvester" : {
            "name" : "harvester",
            "port" : "9350",
            "locations" : "10.10.10.121",
            "doSuspend" : False
        },
        
        "trigger" : {
            "name" : "trigger",
            "port" : "9380",
            "locations" : "10.10.10.131, 10.10.10.132, 10.10.10.133, 10.10.10.134",
            "doSuspend" : False
        },
        
        "mesher" : {
            "name" : "mesher",
            "port" : "9400",
            "locations" : "10.10.14.11, 10.10.10.151, 10.10.10.153, 10.10.10.154, 10.10.10.2, 10.10.12.11",
            "doSuspend" : True
        },
        
        "bounceServer" : {
            "name" : "bounceServer",
            "port" : "9420",
            "locations" : "10.10.10.141",
            "doSuspend" : False
        },
    };
    
    cmd_suspend = "suspend";
    
    def getShellsFolder(self):
        return os.path.abspath(os.path.dirname(sys.argv[0])) + "/shells/";
    
    def getCmdPrefix(self):
        return "/bin/sh " + self.getShellsFolder()+ "call.sh";
    
    def reuseIp(self, diff=7200):
        cmd_list = self.getCmd("mesher", "view ip block info");
        for shell_cmd in cmd_list :
            print self.highlight("execute cmd: " + shell_cmd);
            server_cmd_prefix = shell_cmd.split()[:-4];
            status, result = commands.getstatusoutput(shell_cmd);
            lines = result.splitlines();
            usable_lines = lines[5:len(lines)-2];
            for line in usable_lines :
                detail = line.split();
                blocked_time = datetime.datetime.strptime(" ".join(detail[1:3]), "%Y-%m-%d %H:%M:%S");
                time_diff = datetime.datetime.now() - blocked_time;
                second_diff = time_diff.days * 86400 + time_diff.seconds;
                if second_diff > int(diff) :
                    open_ip_cmd = server_cmd_prefix + ["domain ip open", detail[0], detail[3]];
                    print " ".join(open_ip_cmd);
                    commands.getstatusoutput(" ".join(open_ip_cmd));
            
    
    def getSshPort(self, server_ip):
        server_ip = server_ip.strip();
	if self.ssh_port.get(server_ip) :
            return self.ssh_port.get(server_ip)
        else :
            return "22";
    
    def highlight(self, text):
        return "\033[35;49;1m" + text + "\033[39;49;0m";
    
    def suspend(self, server_name):
        server = self.servers.get(server_name);
        cmd_list = self.getCmd(server.get("name"), self.cmd_suspend);
        print "Suspend server: " + server.get("name");
        for shell_cmd in cmd_list :
            print "execute cmd: " + shell_cmd;
            commands.getstatusoutput(shell_cmd);
        
    def suspendAll(self):
        for server in self.servers.itervalues():
            if(server.get("doSuspend")) :
                self.suspend(server.get("name"));

                             
    def send(self, server_name, cmd):
        server = self.servers.get(server_name);
        cmd_list = self.getCmd(server_name, cmd);
        for shell_cmd in cmd_list :
            print "execute cmd: " + shell_cmd;
            status, result = commands.getstatusoutput(shell_cmd);
            print self.highlight("Reponse is:");
            print result;
                                   
    def sendAll(self, cmd):
        for server in self.servers.itervalues():
            self.send(server.get("name"), cmd);
            
    def getCmd(self, server_name, cmd):
        server_name = self.servers.get(server_name);
        return map(lambda ip :  " ".join((self.getCmdPrefix(), ip, server_name.get("port"), cmd)), server_name.get("locations").split(","));
    
    
    def detectTasks(self):
        hasTasks = False;
        for server in self.servers.itervalues():
            if(server.get("doSuspend")) :
                cmd_list = self.getCmd(server.get("name"), "vt");
                for shell_cmd in cmd_list :
                    status, result = commands.getstatusoutput(shell_cmd);
                    task_size = len(result.splitlines()) - 8;
                    if(task_size > 0):
                        hasTasks = True;
                        print "";
                        print "execute cmd :" + shell_cmd;
                        print "Server: %s, There are still %s tasks in process." % (server.get("name") , self.highlight(str(task_size)));
        return hasTasks;
    
    def stopAll(self):
        for server in self.servers.itervalues():
            self.serviceServer(server.get("name"), "stop");
    
    def restart(self, server_name):
        self.serviceServer(server_name, "restart");
        
    def restartAll(self):
        for server in self.servers.itervalues():
            self.serviceServer(server.get("name"), "restart");
        
    def serviceServer(self, server_name, type):
        server = self.servers.get(server_name);
        cmd_list = map(lambda ip :  " ".join(("ssh -p", self.getSshPort(ip), ip, "service" , server.get("name"), type) ), server.get("locations").split(","));
        for shell_cmd in cmd_list :
            print "execute cmd: " + shell_cmd;
            commands.getstatusoutput(shell_cmd);
    
    '''
        prepare to upgrade.
            1. rsyn all configs to elink_configs at workspace.
            2. suspend all servers except trigger,harvester.
            3. detect task and give a alert when there are no more task.
    '''
    def prepare(self):
        
        '''step 1'''
        print self.highlight("# # Step1 : rsyn configs to elink_configs folder.");
        status, result = commands.getstatusoutput("sh ./shells/rsyn_configs.sh");
        print result;
        
        raw_input("press any key to next step.");
        
        '''step 2'''
        print self.highlight("# # Step2 : suspend all backend server except trigger & harvester.");
        self.suspendAll();
        raw_input("press any key to next step.");

        '''step 3'''
        print self.highlight("# # Step3 : Change Ui to updated vanish mode .");
        status, result = commands.getstatusoutput("sh ./shells/change_ui.sh update");
        raw_input("press any key to next step.");
        
        '''step 4'''
        print self.highlight("# # Step4 :  Now waiting for all inprocessing task to be done.");
        while not self.detectTasks() : 
            print  self.highlight("There still got tasks, next detect will at 1 minute later.");
            time.sleep(60);
        print self.highlight("There are no tasks in processing now.");
        raw_input("press any key to next step.");
        
        """step5 """
        print self.highlight("# # Step5 :  Stop all server now.");
        self.stopAll();
        raw_input("press any key to next step.");
        
        
        print "all server has been shutdown. "
        print "Now pls update source code. "
        

args = sys.argv;
if len(args) == 1 :
    print "pls input the util name you want to call";
else :
    util = UpgradeUtils();  
    method = getattr(util, args[1]);
    result = apply(method, args[2:len(args)]);
    if result:
        print result;
    
    
#util = UpgradeUtils();  
#method = getattr(util, "test");
#apply(method);
