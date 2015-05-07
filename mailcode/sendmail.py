#!/usr/bin/env python3
    #coding: utf-8
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email import Utils
    
    def sendmail(data):
    sender = 'ep_0@sina.com'
    receiver = ['zhahulong@w.cn']
    smtpserver = 'smtp.sina.com'
    username = 'ep_214@sina.com'
    password = 'ho03'
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = '每日报告'
    msgRoot['From'] = sender
    msgRoot['To'] = ';'.join(receiver)
    msgRoot["Date"] = Utils.formatdate(localtime = 1)
    
    html = '''
    <html>
    <head><head>
    <body>
    <p>Hi, all<br>
    <br>
    '''
    for line in data:
    html += '%s %s <br>' % ('&nbsp;'*12, line)
    
    html += '''
    <br>
    顺祝工作愉快！<br>
    <br>
    </body>
    </html>
    '''
    
    # print html
    
    msgText = MIMEText(html, 'html', 'utf-8')
    msgRoot.attach(msgText)
    
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()
