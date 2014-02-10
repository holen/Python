import mdb as mdb
from datetime import datetime, time, timedelta, date
from django.template import loader, Context

today = datetime.combine(datetime.today(), time(0, 0));
yestoday = today - timedelta(days=1);

def get_statd():
    
    stat_sql = '''
        select 
        	"msg_%s_%s_h",h.begin_time,h.from_ip,h.from_inner_ip,h.to_ip,h.error,count(0) as count
		from 
			msg_%s_%s_h h 
		where 
			h.domain_name = '%s' and h.return_type_id = 2
		group by 
			h.error,h.to_ip limit 20
    '''
    
    message_detail = get_all_message();

    display = [];
    for row in message_detail :
        client_id = row["client_id"];
        message_id = row["mail_id"];
        domain_name = row["the_domain"]
        bounce_conn = mdb.get_bounce_conn(client_id);
        domain_stat = mdb.exe_sql(bounce_conn, stat_sql % (client_id, message_id, client_id, message_id, domain_name), True, True);
        display.extend(domain_stat);
        
    print display;

def get_all_message():
    
    find_msg_sql = """
        select 
        	d.client_id,d.mail_id,d.the_domain
		from 
			yulin.day_deliver_report d 
		where 
			d.the_date = '%s' and d.num_fail/(d.num_fail+d.num_success) >= 0.1 and d.num_total >= 100 
			and d.the_domain in ('sina.com')
		order by 
			d.the_domain
    """;       
           
    daily_conn = mdb.get_daily_conn();
    aa = mdb.exe_sql(daily_conn, find_msg_sql % (yestoday), True, True);
    return aa
   
if __name__ == '__main__':  
    get_statd();