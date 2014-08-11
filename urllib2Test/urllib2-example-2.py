#-* coding:UTF-8 -*
#!/usr/bin/env python
import urllib2
import urllib
import cookielib

# urlopen() 创建一个表示远程url的类文件对象，然后像本地文件一样操作这个类文件对象来获取远程数据
response=urllib2.urlopen('http://www.baidu.com')
print response.getcode()
print response.geturl()
message=response.info()
print message.headers
for header in message:
    print header, message.getheader(header)

for header in message:
    print header, message[header]
    pass

print message.getparam('charset')

# urllib.quote()使用适合URL内容的转义序列替换string中的特殊字符。
# 字母、数字、下划线(_)、逗号(,)、句号(.)、连字符(-)都保持不变。其他字符转换成%xx形式的转义序列，默认使用utf-8编码。
# urllib.unquote() 解码
# urllib.urlencode(query) 将query中的查询值转换成一个URL编码的字符串。
# query可以是一个字典，也可以是一个(key,value)的对序列。得到的是以'&'字符分割的'key=value'对序列
form_data={'user':'jhon','passwd':'123456'} #要提交的表单数据
url_data=urllib.urlencode(form_data)        #url_data被编码为'passwd=123456&user=jhon'
full_url='http://www.example.com'+'?'+url_data
u=urllib2.urlopen(full_url)

# urllib2.Request(url [, data [, headers ]]) Request实例可以替代urlopen（url）中的url来实现更加复杂的操作
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}
r=urllib2.Request("http://www.google.com",headers=headers)
u=urllib2.urlopen(r)

#要处理cookie的时候，注意不要在Request里面设置headers，因为cookie也在headers里面，设置headers会将cookie覆盖掉
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
r=urllib2.Request('http://www.google.com')
r.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36')
u=opener.open(r)

# urllib2.urlopen()函数不支持验证、cookie或者其它HTTP高级功能。
# 要支持这些功能，必须使用build_opener()函数创建自定义Opener对象
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
opener.open('http://www.example.com/')

# 密码验证（HTTPBasicAuthHandler）HTTPBasicAuthHandler()处理程序可用add_password()来设置密码。
# h.add_password(realm,uri,user,passwd) realm是与验证相关联的名称或描述信息，取决于远程服务器。uri是基URL。user和passwd分别指定用户名和密码。
auth=urllib2.HTTPBasicAuthHandler()
auth.add_password('Administrator','http://www.example.com','Dave','123456')
opener=urllib2.build_opener(auth)
u=opener.open('http://www.example.com/evilplan.html')

# Cookie处理(HTTPCookieProcessor)
cookie=cookielib.CookieJar()
cookiehand=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(cookiehand)

#代理(ProxyHandler) ProxyHandler(proxies)参数proxies是一个字典，将协议名称（http，ftp）等映射到相应代理服务器的URL。
proxy=urllib2.ProxyHandler({'http':'http://someproxy.com:8080'})
auth=urllib2.lHTTPBasicAuthHandler()
auth.add_password()
opener=urllib2.build_opener(auth,proxy)
#也可以在urlopen中使用代理
proxy = 'http://%s:%s@%s' % ('userName', 'password', 'proxy') 
inforMation = urllib2.urlopen("http://www.example.com", proxies={'http':proxy})   

# http://www.cnblogs.com/linxiyue/p/3537557.html 
