#-* coding:UTF-8 -*
#!/usr/bin/env python
import sys
import mytexttable as nt
import common.mdb as mdb

def showBymessage(start_time, end_time, clients):
    show_sql = '''
        select 
            	ep.client_id,ep.object_id,sum(ep.successful_count),sum(ep.softbounce_count),sum(ep.hardbounce_count),sum(ep.unstart_count)
	from
		email_package ep	
        where 
            	ep.start_time > '%s' and ep.end_time < '%s' and ep.client_id in (%s) 
	group by 
		ep.object_id
    '''
    try:
        carrier_conn = mdb.get_mesher_conn()
        data = mdb.exe_sql(carrier_conn, show_sql % (start_time, end_time, clients), False, True)
	head = ['cid', 'mid', 'success', 'soft', 'hard', 'unstart' ]
	width = [10] * 6
	nt.display(head,data,width)
    except Exception,e:
        print e 
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 4:
        if sys.argv[1] == '-h':
            print("显示客户某个时间段的所有邮件发送情况\nUsage: python %s start_time end_time clients "% sys.argv[0]);
        else:
            start_time = sys.argv[1] 
            end_time = sys.argv[2] 
            clients = sys.argv[3] 
            showBymessage(start_time, end_time, clients)
    else:
    	print("显示客户某个时间段的所有邮件发送情况\nUsage: python %s start_time end_time clients "% sys.argv[0]);
