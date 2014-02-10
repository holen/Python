import common.mdb as mdb
from datetime import datetime, time, timedelta, date
from django.http import HttpResponse
from django.template import loader, Context
from annoying.decorators import render_to
from django.views.decorators.csrf import csrf_exempt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
@render_to('statd/statd.html')
def statd(request, q_type = 'today'):  
	
	day_format = "%Y-%m-%d"
	today = datetime.combine(datetime.today(), time(8, 0));
	yesterday = today - timedelta(hours=32);
	domain = request.POST.get('domain', '')
	domain = '' if domain == "ALL" else domain;
	
	if not q_type:
		q_type = 'yestoday'

	datas = []
	if(q_type == 'today'):
		datas = get_statd(start = datetime.strftime(date.today(), day_format), domain = domain);
	elif(q_type == 'yestoday'):
		datas = get_statd(start = datetime.strftime(yesterday, day_format), domain = domain);
	elif(q_type == 'week'):
		week_ago = date.today() - timedelta(days=7);
		datas = get_statd(start = datetime.strftime(week_ago, day_format), end = datetime.strftime(yesterday, day_format), domain = domain);
	elif(q_type == "custom"):
		start = request.POST["start"];
		end = request.POST["end"];
		message_id = request.POST["msg"];
		datas = get_statd(start = start, end = end, message_id = message_id, domain = domain);
		
	domains = set([data["domain_name"] for data in datas]);
	return locals();


def get_statd(start = None, end = None, branch = None, client = None, message_id = None, domain = None):
	
	stat_sql = '''
		select 
			'%s' as rq, '%s' as branch_id, '%s' as client_id, '%s' as mids, '%s' as subject
			a.domain_name,a.total,a.success,a.success/(a.success+a.soft) as lv,a.soft,a.soft*100/(a.success+a.soft) as sv,
			a.hard,a.hard/a.total as hv,a.block,a.block/a.total as bv,b.dist_ho,b.dist_ho/a.success as ho_lv,c.dist_ct,
			c.dist_ct/a.success as ct_lv 
		from
		(
			select 
				sd.domain_name, 
				sum(sd.group_count) as total,
				sum(if(sd.return_type_id = 1, sd.group_count, 0)) as success,
				sum(if(sd.return_type_id = 2, sd.group_count, 0)) as soft,
				sum(if(sd.return_type_id = 3, sd.group_count, 0)) as hard,
				sum(if(sd.return_type_id = 0, sd.group_count, 0)) as block              
			from 
				summary_%s_delivery sd 
			where 
				sd.message_id in (%s) %s
			group by sd.domain_name 
			order by sd.domain_name desc ) as a 
		left join (
			select 
				domain_name,
				sum(group_count) as ho,
				sum(group_distinct_count) as dist_ho
			from 
				summary_%s_domain_ho  
			where 
				message_id in (%s) %s
			group by domain_name 
			order by domain_name desc ) as b on a.domain_name = b.domain_name
		left join (
			select 
				domain_name,
				sum(group_count) as ct,
				sum(group_distinct_count) as dist_ct
			from 
				summary_%s_domain_ct  
			where 
				message_id in (%s) %s
			group by domain_name 
			order by domain_name desc ) as c on a.domain_name = c.domain_name
	'''
	
	message_detail = get_all_message(start = start, end = end, branch = branch, client = client, message_id = message_id);
	archive_conn = mdb.get_archive_conn();
	
	domain_limit = '' if not domain else " and domain_name = '%s' " % (domain);
	display = [];
	for row in message_detail :
		branch_id = str(row["branch_id"]);
		client_id = str(row["client_id"]);
		message_ids = row["message_ids"];
		format_args = tuple([row["rq"], branch_id, client_id, message_ids, row["subject"].decode('gb2312','replace').encode('utf-8')] + [client_id, message_ids, domain_limit] * 3);
		domain_stat = mdb.exe_sql(archive_conn, stat_sql % (format_args), True);
		display.extend(domain_stat);
		
	mdb.close_conn(archive_conn);
	return display;

def get_all_message(start = None, end = None, branch = None, client = None, message_id = None):
	
	today = datetime.combine(datetime.today(), time(8, 0));
	yestoday = today - timedelta(hours=32);
	
	if(not message_id):
		find_msg_sql = """
			select 
				DATE_FORMAT(m.schedule_time, '%%y-%%m-%%d') as rq, c.branch_id, m.client_id, m.subject, c.client_name, group_concat(m.message_id) as message_ids
			from 
				message m, client c
			where 
				m.client_id = c.client_id and m.begin_time between '%s' and '%s' and m.total_count > 100 and m.status_id = 50
		""";
	else:
		find_msg_sql = '''
			select 
				DATE_FORMAT(m.schedule_time, '%%y-%%m-%%d') as rq, c.branch_id, m.client_id, m.subject, c.client_name, m.message_id as message_ids
			from 
				message m, client c
			where 
				m.client_id = c.client_id and m.message_id = %s
		'''
		
	if(not start):
		start = yestoday;
	elif (not end):
		end = datetime.combine(datetime.strptime(start, "%Y-%m-%d"), time(8, 0)) + timedelta(days=1);
	
	if(not end):
		end = today;
		
	if(client):
		find_msg_sql += " and m.client_id in (%s)" % (client);
	if(branch):
		find_msg_sql += " and c.branch_id in (%s)" % (branch);
		
	find_msg_sql += '''
		group by 
			DATE_FORMAT(m.schedule_time, '%%y-%%m-%%d'), c.client_id, c.client_name, m.subject
		order by
			DATE_FORMAT(m.schedule_time, '%%y-%%m-%%d') asc, c.client_id asc, m.subject asc
	'''
		
	global_conn = mdb.get_global_conn();
	if(not message_id):
		aa = mdb.exe_sql(global_conn, find_msg_sql % (start, end), True, True);
		return aa;
	else:
		aa = mdb.exe_sql(global_conn, find_msg_sql % (message_id), True, True);
		return aa;

	
	
if __name__ == '__main__':  
	statd();