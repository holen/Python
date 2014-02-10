import mdb as mdb
import csv
import os
from datetime import datetime, time, timedelta, date

def getdomain():
	yestoday = date.today() - timedelta(hours=24);

	thesql = '''
		select 
			d.the_date,d.the_domain,sum(d.num_total),sum(d.num_success),sum(d.num_fail),
			sum(d.num_fail)/(sum(d.num_fail)+sum(d.num_success)) as lv,sum(d.num_pingbi),sum(d.num_pingbi)/sum(d.num_total) as uv
		from 
			yulin.day_report d 
		where 
			d.the_date = '%s' and d.the_domain in 
			('qq.com','126.com','163.com','yahoo.com','yahoo.cn','yahoo.com.cn','hotmail.com',
 				'gmail.com','tom.com','21cn.com','sohu.com','sina.com','sina.cn','sina.com.cn')
 		group by 
 			d.the_domain 
 		having 
 			lv > 0.1
 		order by 
 			lv desc
 	'''

 	

