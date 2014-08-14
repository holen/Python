# -*- coding: utf8 -*-
"""
云盘登陆，该类可以登录所有使用360账号登录的网站
@Example
    login = loginYunPan()
    userinfo = login.run('user', 'pwd')
    print userinfo
"""
import sys
import urllib
import urllib2
import cookielib
import time
import random
import hashlib
import json
import re
import os
import poster
 
class loginYunPan():
 
    cookieFile = None
    cookie_jar = None
    serverAddr = None
    userFile = None
 
    def __init__(self):
        self.envInit()
        self.loginInit()
 
    def envInit(self):
        base = sys.path[0] + "/tmp"
        self.userFile = base + '/user.dat'
        self.cookieFile = base + '/cookie.dat'
        if not os.path.isdir(base):
            os.mkdir(base)
        if not os.path.exists(self.userFile):
            open(self.userFile, 'w').close()
        if not  os.path.exists(self.cookieFile):
            open(self.cookieFile, 'w').close()
 
    def loginInit(self):      
        self.cookie_jar  = cookielib.LWPCookieJar(self.cookieFile)
        try:
            self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
        except Exception:
            self.cookie_jar.save(self.cookieFile, ignore_discard=True, ignore_expires=True)
        cookie_support = urllib2.HTTPCookieProcessor(self.cookie_jar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
 
    def getToken(self, username):
        '''根据用户名等信息获得登陆的token值
            username String 用户名
            return 返回Token 值
        '''
        login = {
            'callback' : 'QiUserJsonP1377767974691',
            'func' : 'test',
            'm' : 'getToken',
            'o' : 'sso',
            'rand' : str(random.random()),
            'userName' : username
        }
 
        url = "https://login.360.cn/?"
        queryString = urllib.urlencode(login)
        url += queryString
        result = urllib2.urlopen(url).read()
        #print "result2 : %s" % result
        result = result.strip(' ')
        result = json.loads(result[5:-1])
        token = ''
        if result['errno'] == 0:
            print 'getToken Success'
            token = result['token']
            self.cookie_jar.save(self.cookieFile, ignore_discard=True, ignore_expires=True)
        else:
            print 'getToken Failed, Errno:' + result['errno']
            sys.exit()
        return token
 
    def doLogin(self, username, password, token):
        '''开始执行登陆操作
            username String 用户名
            password String 密码
            token String 根据getToken获得
        '''
        login = {
            'callback' : 'QiUserJsonP1377767974692',
            'captFlag' : '',
            'from' : 'pcw_cloud',
            'func' : 'test',
            'isKeepAlive' : '0',
            'm' : 'login',
            'o' : 'sso',
            'password' : self.pwdHash(password),
            'pwdmethod' : '1',
            'r' : str((long)(time.time()*100)),
            'rtype' : 'data',
            'token' : token,
            'userName' : username
        }
        url = "https://login.360.cn/?"
        queryString = urllib.urlencode(login)
        url += queryString
        result = urllib2.urlopen(url).read()
        #print "result3 : %s" % result
        result = result.replace("\n", '').strip(' ')
        result = json.loads(result[5:-1])
        userinfo = {}
        if result['errno'] == 0:
            print 'Login Success'
            userinfo = result['userinfo']
            open(self.userFile, 'w').write(json.dumps(userinfo))
            self.cookie_jar.save(self.cookieFile, ignore_discard=True, ignore_expires=True)
        else:
            print 'Login Failed, Errno:' + result['errno']
            sys.exit()
        return userinfo
 
 
    def getServer(self):
        '''获得分布式服务器的地址
            return True 已登录 False 未登录
        '''
        url = 'http://yunpan.360.cn/user/login?st=163'
        result = urllib2.urlopen(url).read()
        #print "result1 : %s" % result
        regx = "web : '([^']*)'"
        server = re.findall(regx, result)
        #print "server: %s" % server
        if len(server) and server[0] != '' > 0:
            print "Get Server Success, Server Address:" + server[0]
            self.serverAddr = server[0]
            return True
        else:
            print "Logining!"
            return False
 
    def run(self, username, password):
        '''开始执行登陆流程
            username String 用户名
            password String 密码
        '''
        userinfo = None
        if self.getServer():
            print 'Login Success!'
            userinfo = open(self.userFile).read()
            userinfo = json.loads(userinfo)
            return userinfo
        else:
            # 获取token
            token = self.getToken(username)
            print "token: %s" % token
            # 登陆
            userinfo = self.doLogin(username, password, token);
            # 获得分布式服务器
            self.getServer()
        return userinfo
 
    def pwdHash(self, password):
        '''md5操作函数用于密码加密
            password String 需要加密的密码
            return 加密后的密码
        '''
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()
    
    def upload(self, qid, token):
        '''
            上传文件
        '''
        p = {
                'qid': qid,
                'ofmt': 'json',
                'method': 'Upload.web',
                'token': token,
                'v': '1.0.1',
                'devtype': 'web',
                'pid': 'ajax',
                'Filename': 'ks.cfg',
                'path': '/edata/',
                'file': open('ks.cfg', 'rb'),
                'Upload': 'Submit Query'
                }

        url = "http://up43.yunpan.360.cn/webupload?devtype=web"
        datagen, headers = poster.encode.multipart_encode(p)
        opener = poster.streaminghttp.register_openers()
        opener.add_handler(urllib2.HTTPCookieProcessor(self.cookie_jar))
        urllib2.urlopen(urllib2.Request(url, datagen, headers)).read()
        url_list = "http://c69.yunpan.360.cn/file/list"
        headers_list = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'}
        datagen_dict = {'type': 2, 't': '0.3556266035595015', 'ajax': 1, 'field': 'file_name', 'order': 'asc', 'page': 0, 'page_size': 300, 'path': '/edata/'}
        datagen_list = urllib.urlencode(datagen_dict)
        opener.open(urllib2.Request(url_list, datagen_list, headers_list)).read().decode('utf8')
 
if __name__ == '__main__':
    login = loginYunPan()
    userinfo = login.run('holen2014', 'abcd1234')
    qid = userinfo['qid']
    token = login.getToken('holen2014')
    login.upload(qid, token)
    print userinfo
