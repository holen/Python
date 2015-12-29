#!/usr/bin/python
#coding=UTF-8

#    list_uid, file_name
insert_list_sql = '''
    INSERT INTO `list` (`list_uid`, `list_name`, `list_type_id`, `status_id`, `client_id`, `user_id`, `division_id`, `valid_size`, `invalid_size`, `html_size`,
 `text_size`, `dedup_size`, `public_ind`, `format_id`, `confirm_time`, `notice_email`, `notice_mobile`, `create_user`, `create_time`, `last_update_user`, `last
_update_time`, `last_use_time`)  VALUES ('%s', '%s', 5, 0, 1, 1, %s, 0, 0, 0, 0, 0, 'N', NULL, NULL, NULL, NULL, 1, now(), 0, now(), NULL);
    '''
    
#    format_uid, file_name, relative/file_name
insert_lf_sql = '''
    INSERT INTO `list_format` (`format_uid`, `format_name`, `file_name`, `save_name`, `table_create_sql`, `template`, `client_id`, `list_id`, `xml_file`, `enco
ding`, `email_index`, `title_first`, `delimiter_id`, `bracket_id`, `notify_me`, `notice_email`, `begin_time`, `end_time`) VALUES ('%s', NULL, '%s', '/userfiles
/%s', NULL, '0', NULL, 0, NULL, 'GBK', 0, 'N', 1, 1, 'Y', '', NULL, NULL);
    '''
    
#    xml_key=file_name
insert_lc_sql = '''
    INSERT INTO `list_column` (`format_id`, `client_id`, `list_id`, `status_id`, `column_index`, `ignore_it`, `xml_key`, `attribute_name`, `column_name`, `fiel
d_type_id`, `nullable`, `default_value`, `max_length`, `pointer_len`, `reg_id`, `value_true`, `value_false`, `dynamic`) VALUES (0, 1, 0, 0, 0, 'N', '%s', '邮件
地址', 'email', 1, 'N', NULL, 200, NULL, NULL, NULL, NULL, 'Y');
    '''        
    
#    task_id, remark=file_name
insert_task_sql = '''
    INSERT INTO `task` (`task_id`, `task_name`, `task_type_id`, `service_id`, `task_executor_id`, `language`, `client_id`,`user_id`, `object_id`, `object_flag`
, `group_id`, `task_status_id`, `schedule_time`, `immediately`, `sync`, `start_time`, `end_time`, `priority`, `weight`, `mixed_priority`, `exception`, `restart
_times`, `create_time`, `last_update_time`, `order_number`, `semaphore`, `parameters`, `claimed_process`, `remark`) VALUES ('%s', 'listFormat import', 4, 'load
er', 'import', 'ch', 1, 1, 0, 2, NULL, 10, now(), 'Y', 'Y', now(), NULL, 5, 0, 5, '', NULL, NULL, NULL, 0, 0, '', '10111019310', '%s');
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
    
def import_user_lib(self, path="/tmp/test", division_id=17, start_with='ul'):
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
        
        list_conn = MySQLdb.connect(self.__list_db_host, self.__dbUser, self.__dbPass, self.list_db_name, charset='utf8');
        del_subcribe_sql = [exe_sql(list_conn, 'drop table l%s_subscriber;' % (id), False) for id in to_delete_list_id];
        list_conn.commit();
        close_conn(list_conn);
        
        print in_param;



