#!/usr/bin/python
#coding=UTF-8
'''
Created on 2012-3-11

@author: z
'''
import sys, os;
import re;
import time;
from datetime import datetime, time, date, timedelta;
import MySQLdb;
import texttable as tt;
import uuid
from string import replace
import random
import codecs
import parsexml as parsexml

login_info = parsexml.printxmldata("sewcloud")
mdb_user = login_info['user']
mdb_pass = login_info['passwd']
mdb_ip = login_info['ip']

def exe_sql(connection, sql, closeAfterExecute):
    executor = connection.cursor();
    executor.execute(sql);
    schedule_result = executor.fetchall();
    executor.close();
    if(closeAfterExecute) : 
        connection.close();
    return schedule_result;

def close_conn(connection):
    connection.close();
        
    
def raw_default(prompt, defaultValue=None):
   
    if defaultValue:
        prompt = "%s [ default is -> %s ]: " % (prompt, defaultValue);
        
    schedule_result = raw_input(prompt);
    if not schedule_result and defaultValue:
        return defaultValue
    return schedule_result

def highlight(text):
    return "\033[35;49;1m" + text + "\033[39;49;0m";

class Daily(object):
    
    mesher_db_name = "carrierDB_0";
    global_db_name = "globalDB_0";
    report_db_name = 'reportDB_0';
    archive_db_name = 'archiveDB_0';
    list_db_name = 'listDB_0';
    
    speed_summary_sql = '''
        select 
            DATE_FORMAT(ep.start_time, '%%m-%%d::%%k'), 
            sum(ep.weight),
            sum(ep.successful_count),
            sum(ep.softbounce_count),
            sum(ep.hardbounce_count)
        from 
            email_package ep 
        where 
            ep.task_status_id = 3 and start_time 
            between '%s' and '%s'
        group by 
            DATE_FORMAT(ep.start_time, '%%m-%%d::%%H')
        order by
            ep.start_time
    ''';
    
    yestoday_schedule_summary_sql = '''
        select 
            sum(if(m.status_id=50, 1, 0)) as fc,
            sum(if(m.status_id=50, m.send_count, 0)) as finished,
            sum(if(m.status_id<>50, 1, 0)) as ufc,
            sum(if(m.status_id<>50, m.send_count, 0)) as sending
        from 
            message m
        where 
            m.status_id >= 30 and m.status_id <= 50 
            and m.schedule_time between '%s' and '%s'
    '''
    
    unfinished_msg_summary_sql = '''
        select 
            m.client_id, m.message_id, DATE_FORMAT(m.schedule_time, '%%m-%%d %%k:%%i'), m.send_round, m.send_count
        from 
            message m
        where 
            m.status_id > 30 and m.status_id < 50 
            and m.schedule_time between '%s' and '%s'
        order by 
            m.message_id asc
    '''
    
    unfinished_msg_detail_sql = '''
        select 
            sum(if(ep.task_status_id=3, ep.weight, 0)) as finished,
            sum(if(ep.task_status_id=2, ep.weight, 0)) as sending,
            sum(if(ep.task_status_id=0, ep.weight, 0)) as unstart
        from 
            email_package ep
        where 
            object_id in (%s)
        group by
            object_id
        order by
            object_id asc
    '''
    
    count_18_task_sql = '''
        select object_id from task where object_id in (%s) and task_status_id in (0, 1, 2) and task_type_id in (3, 12, 18)
    '''
    
    def init(self):
        
        reload(sys);
        
        self.__global_db_host = mdb_ip
        self.__archive_db_host = mdb_ip
        self.__dbHost = mdb_ip
        self.__dbUser = mdb_user
        self.__dbPass = mdb_pass
        
        self.__report_db_host = mdb_ip
        self.__list_db_host = mdb_ip
        
        self.__today = datetime.combine(datetime.today(), time(0, 0));
        self.__yestoday = self.__today - timedelta(days=1);
#        self.__conn = MySQLdb.connect(self.__dbHost, self.__dbUser,  self.__dbPass, self.__dbName, charset='utf8');
        
    def speed(self, start_time=None, end_time=None):
        
#        today = time.strftime("%Y-%m-%d", time.localtime());
        
        if(not start_time):
            start_time = datetime.combine(self.__yestoday, time(18, 0));
        
        if(not end_time):
            end_time = datetime.now();
            
        
        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.mesher_db_name, charset='utf8');
        schedule_result = list(exe_sql(conn, self.speed_summary_sql % (start_time, end_time), True));
        tr_result = map(list, zip(*schedule_result));
        total = map(sum, tr_result[1:]);
        average = map(lambda x : x / len(schedule_result), total);
        schedule_result.append(["Average"] + average);
        schedule_result.append(["Total"] + total);
        
        self.display(['Hour', 'Total', 'success', 'soft-bounce', 'hard-bounce'], schedule_result, ["l", "c", "c", "c", "c"]);
    
#    默认统计昨天的邮件完成情况
    def summary(self, start_time=None, end_time=None):
        
        if(not start_time):
            start_time = self.__yestoday;
        elif (not end_time):
            end_time = datetime.combine(datetime.strptime(start_time, "%Y-%m-%d"), time(0, 0)) + timedelta(days=1);
        
        if(not end_time):
            end_time = self.__today;
        
        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.global_db_name, charset='utf8');
        # print self.yestoday_schedule_summary_sql % (start_time, end_time)
        schedule_result = exe_sql(conn, self.yestoday_schedule_summary_sql % (start_time, end_time), False);
        
        print " ".join(("\nMessages scheduled From", str(start_time), 'to', str(end_time), '\n'));
        self.display(['Finished', 'Finished amount', 'Unfinished', 'Unfinished amount'], schedule_result);
        
        unfinished_msg_result = list(exe_sql(conn, self.unfinished_msg_summary_sql % (start_time, end_time), True));
	#print unfinished_msg_result
        
        result = [];
        if len(unfinished_msg_result) > 0:
            
            unfinished_msg_id = [str(i[1]) for i in unfinished_msg_result];
            conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.mesher_db_name, charset='utf8');
            detail_result = exe_sql(conn, self.unfinished_msg_detail_sql % (",".join(unfinished_msg_id)), True);
	    #print detail_result
            result = map(lambda x, y : list(x) + list(y) , list(unfinished_msg_result), list(detail_result));
            
#            result = [];
#            for i in range(0, len(unfinished_msg_id) - 1) :
#                result.append(list(unfinished_msg_result[i]) + list(detail_result[i]));
            
            print '\n\nThe Unfinished Message detail.\n'
            tr_result = map(list, zip(*result));
            result.append(['total', '', ''] + map(sum, tr_result[3:]));
            
            self.display(['Cid', 'Mid', 'Schedule on', 'Round', 'Send Count', 'Finished', 'Sending', 'Unstart'], result);
            
        
#        假如 Unstart Count 为 0， 检查task表的未完成 18号任务
        #print "\nall ids:" + ",".join([str(m[0]) for m in result]);
        #no_unstart_msg_ids = [str(m[0]) for m in result if m[5] == 0 and m[6] == 0];
        #if len(no_unstart_msg_ids):
        #    conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.global_db_name, charset='utf8');
        #    waiting_msg_ids = exe_sql(conn, self.count_18_task_sql % (",".join(no_unstart_msg_ids)), True);
        #    un_normal_ids = filter(lambda id: int(id) not in [column[0] for column in waiting_msg_ids], no_unstart_msg_ids);
        #    print "Finished ids:" + ",".join(no_unstart_msg_ids);
        #    print "Waiting  ids:" + ",".join([str(id[0]) for id in waiting_msg_ids]);
        #    for id in un_normal_ids:
        #        print 'direct to report for ' + id;
        #    print "\n\n"
            
    
    def priority(self, diff=5, priority=1):
        
        sql = '''
            update 
                email_package ep
            set 
                ep.priority = %s
            where 
                ep.task_status_id = 0
                and ep.schedule_time < '%s';
            commit;
        '''
        
        when = datetime.now() - timedelta(hours=int(diff));
        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.mesher_db_name, charset='utf8');
        result = exe_sql(conn, sql % (int(priority), when), True);
        print result;
        
    def imt(self, message_id, priority=1):
        sql = '''
            update email_package ep set ep.priority = %s where ep.task_status_id = 0 and ep.object_id in (%s);
        '''
        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.mesher_db_name, charset='utf8');
        result = exe_sql(conn, sql % (int(priority), message_id), False);
        conn.commit();
        close_conn(conn);
        print result;
        
    
#    list_uid, file_name
    insert_list_sql = '''
    INSERT INTO `list` (`list_uid`, `list_name`, `list_type_id`, `status_id`, `client_id`, `user_id`, `division_id`, `valid_size`, `invalid_size`, `html_size`, `text_size`, `dedup_size`, `public_ind`, `format_id`, `confirm_time`, `notice_email`, `notice_mobile`, `create_user`, `create_time`, `last_update_user`, `last_update_time`, `last_use_time`)  VALUES ('%s', '%s', 5, 0, 1, 1, %s, 0, 0, 0, 0, 0, 'N', NULL, NULL, NULL, NULL, 1, now(), 0, now(), NULL);
    '''
    
#    format_uid, file_name, relative/file_name
    insert_lf_sql = '''
    INSERT INTO `list_format` (`format_uid`, `format_name`, `file_name`, `save_name`, `table_create_sql`, `template`, `client_id`, `list_id`, `xml_file`, `encoding`, `email_index`, `title_first`, `delimiter_id`, `bracket_id`, `notify_me`, `notice_email`, `begin_time`, `end_time`) VALUES ('%s', NULL, '%s', '/userfiles/%s', NULL, '0', NULL, 0, NULL, 'GBK', 0, 'N', 1, 1, 'Y', '', NULL, NULL);
    '''
    
#    xml_key=file_name
    insert_lc_sql = '''
    INSERT INTO `list_column` (`format_id`, `client_id`, `list_id`, `status_id`, `column_index`, `ignore_it`, `xml_key`, `attribute_name`, `column_name`, `field_type_id`, `nullable`, `default_value`, `max_length`, `pointer_len`, `reg_id`, `value_true`, `value_false`, `dynamic`) VALUES (0, 1, 0, 0, 0, 'N', '%s', '邮件地址', 'email', 1, 'N', NULL, 200, NULL, NULL, NULL, NULL, 'Y');
    '''        
    
#    task_id, remark=file_name
    insert_task_sql = '''
    INSERT INTO `task` (`task_id`, `task_name`, `task_type_id`, `service_id`, `task_executor_id`, `language`, `client_id`,`user_id`, `object_id`, `object_flag`, `group_id`, `task_status_id`, `schedule_time`, `immediately`, `sync`, `start_time`, `end_time`, `priority`, `weight`, `mixed_priority`, `exception`, `restart_times`, `create_time`, `last_update_time`, `order_number`, `semaphore`, `parameters`, `claimed_process`, `remark`) VALUES ('%s', 'listFormat import', 4, 'loader', 'import', 'ch', 1, 1, 0, 2, NULL, 10, now(), 'Y', 'Y', now(), NULL, 5, 0, 5, '', NULL, NULL, NULL, 0, 0, '', '10111019310', '%s');
    '''
    
    update_lf_sql = '''
    update list_format lf, list l set lf.list_id = l.list_id where l.list_name = '%s' and l.list_name = lf.file_name;
    '''
    
    update_lc_sql = '''
    update list_column lc, list_format lf set lc.list_id = lf.list_id, lc.format_id = lf.format_id where lf.file_name = '%s' and lf.file_name = lc.xml_key;
    '''
    
    update_t_sql = '''
    update list_format lf, task t set t.object_id = lf.list_id, t.parameters = concat('list_format_id="', lf.format_id,'";'),t.task_status_id = 0 where lf.file_name = '%s' and t.remark = lf.file_name;
    '''
    
    def import_user_lib(self, path="C:\\test", division_id=17, start_with='ul'):
        random_container = 'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba0123456789'
        base_path = '/userfiles/';
        index_of_base = path.index(base_path);
        relative_path = path[index_of_base:].replace(base_path, '');
        
        targets = os.listdir(path);
        
        il_sql_list = [self.insert_list_sql % (str(uuid.uuid1()).replace('-', ''), f, division_id) for f in targets if str(f).startswith(start_with)];
        ilf_sql_list = [self.insert_lf_sql % (str(uuid.uuid1()).replace('-', ''), f, relative_path + os.path.sep + f) for f in targets if str(f).startswith(start_with)];
        ilc_sql_list = [self.insert_lc_sql % (f) for f in targets if str(f).startswith(start_with)];
        it_sql_list = [self.insert_task_sql % (''.join(random.sample(random_container, 8)), f) for f in targets if str(f).startswith(start_with)];
        ulf_sql_list = [self.update_lf_sql % (f) for f in targets if str(f).startswith(start_with)];
        ulc_sql_list = [self.update_lc_sql % (f) for f in targets if str(f).startswith(start_with)];
        ut_sql_list = [self.update_t_sql % (f) for f in targets if str(f).startswith(start_with)];
        
        print "\n".join(il_sql_list);
        print "\n".join(ilf_sql_list);
        print "\n".join(ilc_sql_list);
        print "\n".join(it_sql_list);
        print "\n".join(ulf_sql_list);
        print "\n".join(ulc_sql_list);
        print "\n".join(ut_sql_list);
        
        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.global_db_name, charset='utf8');
        conn.autocommit(True);
##        exe_sql(conn, "\n".join(il_sql_list) + "\n".join(ilf_sql_list) + "\n".join(ilc_sql_list) + "\n".join(it_sql_list) + "\n".join(uu_sql_list), True);
        [exe_sql(conn, sql, False) for sql in il_sql_list];
        [exe_sql(conn, sql, False) for sql in ilf_sql_list];
        [exe_sql(conn, sql, False) for sql in ilc_sql_list];
        [exe_sql(conn, sql, False) for sql in it_sql_list];
        [exe_sql(conn, sql, False) for sql in ulf_sql_list];
        [exe_sql(conn, sql, False) for sql in ulc_sql_list];
        [exe_sql(conn, sql, False) for sql in ut_sql_list];
#        exe_sql(conn, "\n".join(ilf_sql_list), False);
#        exe_sql(conn, "\n".join(ilc_sql_list), False);
#        exe_sql(conn, "\n".join(it_sql_list), False);
#        exe_sql(conn, "\n".join(uu_sql_list), False);
        close_conn(conn);
        
    def delete_ul(self, name="ul_live"):
        find_list_sql = 'select l.list_id from list l where l.list_name like "' + name + '%"';
        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.global_db_name, charset='utf8');
        to_delete_list_id = [str(i[0]) for i in exe_sql(conn, find_list_sql, False)];
        
        in_param = ",".join(to_delete_list_id);
        
        del_lc_sql = 'delete from list_column where list_id in (' + in_param + ');';
        del_lf_sql = 'delete from list_format where list_id in (' + in_param + ');';
        del_l_sql = 'delete from list where list_id in (' + in_param + ');';
        exe_sql(conn, del_lc_sql, False);
        exe_sql(conn, del_lf_sql, False);
        exe_sql(conn, del_l_sql, False);
        conn.commit();
        close_conn(conn);
#        print del_lc_sql;
#        print del_lf_sql;
#        print del_l_sql;
        
        list_conn = MySQLdb.connect(self.__list_db_host, self.__dbUser, self.__dbPass, self.list_db_name, charset='utf8');
        del_subcribe_sql = [exe_sql(list_conn, 'drop table l%s_subscriber;' % (id), False) for id in to_delete_list_id];
        list_conn.commit();
        close_conn(list_conn);
        
        print in_param;
        

    def export_ho(self):
        
        find_tables_sql = 'show tables like "%_ho"';
        sql = r'''
            select ho.email_address from %s ho into outfile '/home/z/ho/%s.csv' fields terminated by ',' optionally enclosed by '"' escaped by '"'  lines terminated by '\r\n';
        '''
        conn = MySQLdb.connect(self.__report_db_host, self.__dbUser, self.__dbPass, self.report_db_name, charset='utf8');
        to_export = exe_sql(conn, find_tables_sql, False);
        result = [exe_sql(conn, sql % (tbl[0], tbl[0]), False) for tbl in to_export];
        close_conn(conn);
        
            
    def statd(self, start = None, end = None, branch = None, client = None):
        
        find_msg_sql = """
            select 
                DATE_FORMAT(m.schedule_time, '%%m-%%d'), m.client_id, c.client_name, group_concat(m.message_id) 
            from 
                message m, client c
            where 
                m.client_id = c.client_id 
                and m.end_time between '%s' and '%s'
        """;
        
        
        if(not start):
            start = self.__yestoday;
        elif (not end):
            end = datetime.combine(datetime.strptime(start, "%Y-%m-%d"), time(0, 0)) + timedelta(days=1);
        
        if(not end):
            end = self.__today;
        
        if(client):
            find_msg_sql += " and m.client_id in (%s)" % (client);
        if(branch):
            find_msg_sql += " and c.branch_id in (%s)" % (branch);
            
        find_msg_sql += '''
            group by 
                DATE_FORMAT(m.schedule_time, '%%m-%%d'), c.client_id, c.client_name 
            order by
                DATE_FORMAT(m.schedule_time, '%%m-%%d') asc
        '''
            
        #conn = MySQLdb.connect(self.__global_db_host, self.__dbUser, self.__dbPass, self.global_db_name, 60001, charset='utf8');
        conn = MySQLdb.connect(self.__global_db_host, self.__dbUser, self.__dbPass, self.global_db_name, charset='utf8');
        splited = exe_sql(conn, find_msg_sql % (start, end), True);
        
        
        stat_sql = '''
            select 
                domain_name, 
                sum(group_count) as total,
                sum(if(return_type_id = 1, group_count, 0)) as success,
                sum(if(return_type_id = 2, group_count, 0)) as soft,
                sum(if(return_type_id = 3, group_count, 0)) as hard,
                sum(if(return_type_id = 0, group_count, 0)) as block
            from summary_%s_delivery 
            where message_id in (%s) 
            group by domain_name 
            order by total desc 
        '''
        
        header = codecs.BOM_UTF8 + "日期,客户编号,客户名称,发送域,发送总量,发送成功量,发送失败量,硬退量,屏蔽量"
#        header = "日期,客户编号,客户名称,发送域,发送总量,发送成功量,发送失败量,硬退量,屏蔽量";
        print header;
        
        archive_conn = MySQLdb.connect(self.__archive_db_host, self.__dbUser, self.__dbPass, self.archive_db_name, charset='utf8');
        for target in splited:
            day = target[0];
            client_id = target[1];
            client_name = target[2];
            message_id = target[3];
            result = [",".join([day, str(client_id), client_name] + map(lambda a : str(a), row)) for row in exe_sql(archive_conn, stat_sql % (client_id, message_id), False)];
            print "\n".join(result).encode("utf-8");
        
        if archive_conn:
            close_conn(archive_conn);
            
            
    def merge_archive(self):
        
        sql = """
            select 
                m.client_id, mg.group_id, group_concat(m.message_id)
            from 
                message m, message_group mg 
            where 
                m.group_id=mg.group_id and m.client_id in (3,4,5,6,7,8,9,10,11,14,14,19,26,27,30) 
            group by m.client_id, m.group_id 
            order by m.client_id, m.group_id 
        """
        
        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.global_db_name, charset='utf8');
        splited = exe_sql(conn, sql, True);

        
        tar_cmd = "tar -zcvf %d.tgz %s";
        target_list = [];
        
        for target in splited:
            client_id = target[0];
            group_id = target[1];
            message_list = target[2].split(",");
            cmd_list = [ (str(client_id) + "/"+ str(message) + ".zip") for message in message_list]
            target_line = " ".join(cmd_list);
            
            print tar_cmd % (group_id, target_line);
        
        
        
    
    def display(self, header, data, cols=None):
        if not cols:
            cols = ['c'] * len(header);
            
        display_schedule_tbl = tt.Texttable();
        display_schedule_tbl.set_cols_align(cols);
        display_data = [header];
        display_data.extend(data);
        display_schedule_tbl.add_rows(display_data);
        display = display_schedule_tbl.draw();  
        print display;
        return display;
        
    def unfinish(self, mid=None, start_time=None):
        sql = '''
            select 
                ep.client_id,ep.object_id,ep.schedule_time,ep.domain_name,ep.claimed_process,sum(ep.weight)
            from 
                email_package ep where ep.task_status_id < 3 
        '''

        if mid :
            sql += " and ep.object_id = %s " % mid

        if start_time:
            sql += ''' and ep.schedule_time >= '%s' ''' % start_time

        if (not mid) and (not start_time):
            sql += ''' and ep.schedule_time >= '%s' ''' % self.__yestoday
        
        sql += ''' group by ep.object_id,ep.domain_name '''

        conn = MySQLdb.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.mesher_db_name, charset='utf8');
        result = list(exe_sql(conn, sql, True))
        self.display(['Cid', 'Mid', 'Stime', 'Domain', 'Claimed', 'Weight'], result);

if __name__ == '__main__':
   
    daily = Daily();
    daily.init();
        
    args = sys.argv;
    if len(args) == 1 :
        schedule_result = daily.merge_archive();
    else:
        method = getattr(daily, args[1]);
        real_arg = args[2:len(args)];
        if(len(args) > 2 and str(real_arg[0]).find('=') > 0):
            kw = {};
            for arg in real_arg:
                splited = arg.split('=');
                kw[splited[0]] = splited[1];
            apply(method, (), kw);
        else:
            schedule_result = apply(method, real_arg);

