#!/usr/bin/python
#coding=UTF-8
'''
Created on 2012-3-11

@author: holen
'''
import sys
import mdb as mdb
import getcid as gcid
import texttable as tt;

def display(header, data, cols=None):
    if not cols:
        cols = ['c'] * len(header);        
    display_schedule_tbl = tt.Texttable();
    # display_schedule_tbl.set_cols_width([10,15,14,13,15,50,5]);
    display_schedule_tbl.set_cols_width([5,5,5,5,5,50,5]);
    display_schedule_tbl.set_cols_align(cols);
    display_data = [header];
    display_data.extend(data);
    display_schedule_tbl.add_rows(display_data);
    display = display_schedule_tbl.draw();  
    print display;

def get_bounceinfo(cid, mid, domain, group='error', lid = None):
	get_data = '''
		select 
			"%s_%s", substring(h.real_from,instr(h.real_from,'@')+1) as real_from, h.from_ip, h.from_inner_ip, to_ip, h.error, count(0) 
		from 
			msg_%s_%s_h h 
		where
			h.domain_name = '%s' and h.return_type_id = 2
	'''

	if lid:
		get_data += ''' and h.list_id = 0 '''

	get_data += '''
		group by 
			%s 
		order by 
			count(0) 
	'''

	# print get_data	% (cid, mid, cid, mid, domain, group)
	bounce_conn = mdb.get_bounce_conn(cid);
	datas = mdb.exe_sql(bounce_conn, get_data % (cid, mid, cid, mid, domain, group), False, True)
	# display(['msg','real_from','from_ip','from_inner_ip','to_ip','error','count'], datas, ["c","c", "c", "c", "c", "l", "c"])
	display(['msg','rfrom','wip','lip','toip','error','count'], datas, ["c","c", "c", "c", "c", "l", "c"])

if __name__ == '__main__':
        if len(sys.argv) < 3 :
            print("查询一封邮件特定域的错误信息\nUsage: python %s message_id domain [error_type] [list_id] " % sys.argv[0]);
            sys.exit()
        message_id = sys.argv[1]
        client_id = gcid.getcid(int(message_id))
        domain = sys.argv[2]
        if len(sys.argv) == 4 :
            group = sys.argv[3]
            if sys.argv[3] == 'real_from':
                group = 'substring(h.real_from,instr(h.real_from,"@")+1)'
        else :
            group = 'error'
        if len(sys.argv) == 5:
            list_id = sys.argv[4]
	    get_bounceinfo(client_id, message_id, domain, group, list_id)
        else :
            get_bounceinfo(client_id, message_id, domain, group)
