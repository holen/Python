import common.mdb as mdb
from datetime import datetime, time, timedelta, date
from django.http import HttpResponse
from django.template import loader, Context
from annoying.decorators import render_to
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@render_to('analyse/analyse.html')
def analyse(request, branch_id, client_id, message_ids, domain, subject, group = False):  
    
    reports = []
    reports = get_analyse(branch_id, client_id, message_ids, domain);
    return locals();
        
def get_analyse(branch_id, client_id, message_ids, domain, group = False):
    
    stat_sql = '''
        select 
           '%s' as message_id, DATE_FORMAT(h.begin_time, '%%Y-%%m-%%d %%H:%%i') as begin_time, substring(h.real_from,instr(h.real_from,'@')+1) as real_from, h.from_ip, h.from_inner_ip, h.to_ip, h.error, count(0) as count
        from 
            msg_%s_%s_h h 
        where 
            h.domain_name = '%s' and h.return_type_id = 2
        '''

    if(group):
        stat_sql += '''group by %s''' % (group)
    else:
        stat_sql += '''group by h.error '''

    stat_sql += '''order by count desc limit 20'''

    bounce_conn = mdb.get_bounce_conn(client_id);
    
    display = [];
    messages = message_ids.split(',')
    for message in messages:
        domain_stat = mdb.exe_sql(bounce_conn, stat_sql % (message, client_id, message, domain), True);
        display.extend(domain_stat);
                
    mdb.close_conn(bounce_conn);
    return display;    
    
if __name__ == '__main__':  
    analyse();