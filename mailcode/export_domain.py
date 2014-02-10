#!/usr/bin/python
#coding: utf-8 
import mdb as mdb
import csv
import os, sys
from datetime import datetime, time, timedelta, date
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email import Utils,Encoders  

def get_error_mail():
	yestoday = date.today() - timedelta(hours=24);

	get_error_sql = '''
		select 
			dr.the_domain, group_concat(dr.client_id) as cids, group_concat(dr.mail_id) as mids
		from 
			day_deliver_report dr 
		where 
			dr.the_date = '%s' and dr.num_total > 100 and dr.per_fail > 0.1 
			and dr.the_domain in ('qq.com','vip.qq.com','sina.com','sina.com.cn','sina.cn','163.com','126.com','sohu.com','yeah.net',
				'yahoo.com','yahoo.com.cn','yahoo.cn','21cn.com','139.com','gmail.com','tom.com','hotmail.com','vip.sina.com')
		group by 
			dr.the_domain
		order by 
			dr.client_id;
	'''

	report_conn = mdb.get_error_conn();
	datas = mdb.exe_sql(report_conn, get_error_sql % (yestoday), True, True);
	return datas;

def export():
	yestoday = date.today() - timedelta(hours=24);
	datas = get_error_mail();

	the_sql = '''
		select 
			"msg_%s_%s_h", h.begin_time, h.real_from, h.from_ip, h.from_inner_ip, h.to_ip, h.error, count(0) as count
		from 
			msg_%s_%s_h h 
		where 
			h.domain_name = '%s' and h.return_type_id = 2
		group by 
			error
		order by 
			count desc 
		limit 20;
	'''

	result = []

	the_dir = "C:\\Users\\huilong.zhang\\Desktop\\%s" % (yestoday);
	
	if os.path.exists(the_dir) :
		os.rename(the_dir,'%s.bak' % (the_dir))
	
	os.mkdir('%s' % (the_dir))
	os.chdir('%s' % (the_dir))

	for data in datas:
		domain    = data["the_domain"]
		cids      = data["cids"];
		mids      = data["mids"]
		client_id = cids.split(',')
		message   = mids.split(',')
		the_file  = '%s-%s.csv' % (domain,yestoday)
		csvfile   = file('%s' % (the_file), 'ab')
		writer    = csv.writer(csvfile)
		writer.writerow(['msg_h', 'begin_time', 'real_from', 'from_ip', 'from_inner_ip', 'to_ip', 'error', 'count'])
		for i in range(len(client_id)):
			bounce_conn = mdb.get_bounce_conn(client_id[i]);
			reports = mdb.exe_sql(bounce_conn, the_sql % (client_id[i], message[i], client_id[i], message[i], domain), False, True);
			writer.writerows(reports)

		csvfile.close();

def sendMail():
	sender = 'huilong.zhang@epcare.com.cn'  
	receiver = ['zhiping.chen@epcare.com.cn', 'wenqian.xie@epcare.com.cn', 'huilong.zhang@epcare.com.cn', 'weizhao.tang@epcare.com.cn', 'yongkun.liao@epcare.com.cn']
	# receiver = ['huilong.zhang@epcare.com.cn']
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

if __name__ == '__main__':  
	export();
	sendMail();