#!/usr/bin/env python3  
#coding: utf-8  
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email import Utils,Encoders  
import os, sys
from datetime import datetime, time, timedelta, date
  
sender = 'huilong.zhang@epcare.com.cn'  
receiver = ['huilong.zhang@epcare.com.cn', '823772686@qq.com']
smtpserver = 'mail.epcare.com.cn'  
username = 'huilong.zhang@epcare.com.cn'  
password = 'epcare2012zh1'  
yestoday = date.today() - timedelta(hours=24);
  
msgRoot = MIMEMultipart('related') 
msgRoot['Subject'] = '每日域报告'  
msgRoot['From'] = sender
msgRoot['To'] = ';'.join(receiver)
msgRoot["Date"] = Utils.formatdate(localtime = 1)
  
#文本内容
# text = '''
# Hi, all

#     以上是昨天各个域的发送情况，详看附件！

# 顺祝工作愉快！
# '''
# content = MIMEText(text, 'plain', 'utf-8')
# msgRoot.attach(content)
html = '''
<html>
    <head><head>
    <body>
        <p>Hi, all<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;以上是昨天各个域的发送情况，详看附件！<br>
            <br>
            顺祝工作愉快！<br>
            <br>
            <img src="cid:image1">
        </p>
    </body>
</html>
'''
msgText = MIMEText(html, 'html', 'utf-8')
msgRoot.attach(msgText)
fp = open('D:\\me.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

#构造附件  
the_dir = 'C:\\Users\\huilong.zhang\\Desktop\\%s\\' % yestoday
if os.path.exists(the_dir) :
    os.chdir('%s' % (the_dir))
else:
    print 'no %s' % the_dir
    sys.exit() 

for dirfile in os.listdir(the_dir):
    if os.path.isfile(dirfile):
        csvfile = open(dirfile, 'rb')
        att = MIMEText(csvfile.read(), 'base64', 'utf-8')  
        csvfile.close()
        att["Content-Type"] = 'application/octet-stream'  
        att["Content-Disposition"] = 'attachment; filename="%s"'  % dirfile
        msgRoot.attach(att)  
          
smtp = smtplib.SMTP()  
smtp.connect(smtpserver)  
smtp.login(username, password)  
smtp.sendmail(sender, receiver, msgRoot.as_string())  
smtp.quit()  