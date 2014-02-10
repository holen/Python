#!/usr/bin/python
import imaplib, string, email
from email.parser import Parser
from email.Utils import parseaddr
from email.Header import decode_header
import re, sys
from datetime import datetime, timedelta, time
import mdb as mdb

def getmailheader(header_text, default="ascii"):
    """Decode header_text if needed"""
    try:
        headers=decode_header(header_text)
    except email.Errors.HeaderParseError:
        # This already append in email.base64mime.decode()
        # instead return a sanitized ascii string 
        return header_text.encode('ascii', 'replace').decode('ascii')
    else:
        for i, (text, charset) in enumerate(headers):
            try:
                headers[i]=unicode(text, charset or default, errors='replace')
            except LookupError:
                # if the charset is unknown, force default 
                headers[i]=unicode(text, default, errors='replace')
        return u"".join(headers)

def USToLocaltime(TIME1):
    """Format the time
    e.g. 'Thu, 15 Dec 2011 17:04:56 +0800 (CST)'-->'2011-12-15 17:04:56'
    """    
    if ('+0800' in TIME1):
        CST0_FORMAT = '%a, %d %b %Y %H:%M:%S +0800'
        dt=datetime.strptime(TIME1, CST0_FORMAT)
        #dt=time.strptime(str(dt1),'%Y-%m-%d %H:%M:%S')
        #dt=time.mktime(datetime.datetime(dt[0],dt[1],dt[2]+1,dt[3]-16,dt[4],dt[5]).timetuple())
        #dt=time.strftime('%m/%d/%Y %I:%M:%S %p',time.gmtime(float(dt)))    
        return dt        
    elif ('+0800 (CST)' in TIME1 and 'CST' in TIME1):    
        CST0_FORMAT = '%a, %d %b %Y %H:%M:%S +0800 (CST)'
        dt=datetime.strptime(TIME1, CST0_FORMAT)
        return dt        
    elif ('-0500' in TIME1):    
        CST0_FORMAT = '%a, %d %b %Y %H:%M:%S -0500 (EST)'#-0800
        dt=datetime.strptime(TIME1, CST0_FORMAT)
        return dt        
    elif ('-0800' in TIME1):    
        CST0_FORMAT = '%a, %d %b %Y %H:%M:%S -0800 (PST)'
        dt=datetime.strptime(TIME1, CST0_FORMAT)
        return dt        
    else:    
        UTC_FORMAT = '%a, %d %b %Y %H:%M:%S +0800'
        datetime.utcnow().strftime(UTC_FORMAT)
        return datetime.strptime(TIME1, UTC_FORMAT)

def LocaltimetoUs(TIME1):
    """ Format the time 
    e.g. '2013-06-06' --> '6-Jun-2013'
    """
    try:
        CST0_FORMAT = '%d-%b-%Y'
        a = datetime.datetime.strptime(TIME1, '%Y-%m-%d').date()
        dt = a.strftime(CST0_FORMAT)
        return dt
    except Exception, e:
        print "Format time error: %s" %e

def loginIMAP(email_address, domain_name, pwd):
    """Login the imap """
    if domain_name == "sohu.com":
        M = imaplib.IMAP4("mail.sohu.com")
    else:
        M = imaplib.IMAP4("imap.%s" % domain_name) 
    try:
        M.login(email_address, pwd)
        return M
    except Exception, e:
        print 'login error:%s' %e
        M.close()
        sys.exit(1)

def getSeedemail():
    get_seed_sql = '''
        select 
            ge.email_address,ge.domain_name,ge.password 
        from 
            global_seed_emails ge 
        where 
            ge.domain_name in ('163.com', '126.com', 'sina.com', 'sina.cn', 'sohu.com')
        order by
            ge.domain_name;
    '''
    try:
        get_seed_conn = mdb.get_vmware_conn()
        datas = mdb.exe_sql(get_seed_conn, get_seed_sql, True, True)
        return datas
    except Exception, e:
        print 'Get data from Mysql error: %s' %e

def insertData(data):
    insert_sql = '''
        INSERT INTO `headerinfo1` 
            (`re_time`, `uid`, `mid`, `box_status`, `from_addree`, `seed_email`, `domain_name`, `sender`, `subject`, `box_id`) 
        VALUES 
            ('%s', %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s');
    '''
    try:
        insert_conn = mdb.get_vmware_conn()
        datas = mdb.exe_sql(insert_conn, insert_sql % data, False, True)
    except Exception, e:
        print 'Insert data to Mysql error: %s' %e

def getEmailuid(email_address):
    get_maxid_sql = '''
        select 
            max(h.box_id) as max_uid
        from 
            headerinfo1 h 
        where 
            h.seed_email = '%s'
    '''
    try:
        select_conn = mdb.get_vmware_conn()
        uid = mdb.exe_sql(select_conn, get_maxid_sql % email_address, True, True)
        return uid[0]['max_uid']
    except Exception, e:
        print 'Select the max uid error: %s' %e

def parseMailHeader(email_address, domain_name, pwd='qwer1234'):
    """Parse the Mail Header to get the subject, from, to, X-Reply-to and so on ..."""
    # today = datetime.today()
    # yestoday = today - timedelta(days=1)
    # before_time = today.strftime("%d-%b-%Y")
    # since_time = yestoday.strftime("%d-%b-%Y")

    try:
        M = loginIMAP(email_address, domain_name, pwd)
        if domain_name == 'sina.cn' or domain_name == 'sina.com':
            box_array = ['INBOX', '&i6KWBZCuTvY-', '&V4NXPpCuTvY-']
        elif domain_name == 'sohu.com':
            box_array = ['INBOX', 'Spam']
        else:
            box_array = ['INBOX', '&Xn9USpCuTvY-', '&i6KWBZCuTvY-', '&V4NXPpCuTvY-']
        max_uid = getEmailuid(email_address)
        print email_address, max_uid
        for box in box_array:
            if box == "INBOX":
                box_status = 1
            elif box == "&Xn9USpCuTvY-":
                box_status = 2
            elif box == "&i6KWBZCuTvY-":
                box_status = 3
            else:
                box_status = 4
            result, message = M.select(box)
            # typ, data = M.search(None, '(SINCE %s BEFORE %s)' % (since_time, before_time) )
            typ, data = M.uid('search', None, 'ALL')
            print data
            if not data[0]:
                continue
            # for num in [string.split(data[0])[-1]]:
            for num in string.split(data[0]):
                if int(num) > int(max_uid):
                    # print num
                # if int(num) > 0:
                    try:
                        header_info = []
                        if domain_name == 'sohu.com':
                            typ, data = M.uid('fetch', num, '(RFC822)')
                        else:
                            typ, data = M.uid('fetch', num, '(RFC822.HEADER)')
                            # typ,data = M.fetch(num, '(RFC822.HEADER)')
                        msg = email.message_from_string(data[0][1])
                        reply = msg.get('X-Reply-to', '')
                        if reply != "":
                            reply_array = reply.split('/')
                            user_id = reply_array[3]
                            # print user_id
                            message_id = reply_array[2] 
                            # print message_id
                            subject = getmailheader(msg.get('Subject', ''))
                            # print subject
                            the_from = msg.get('From', '')
                            from_address = re.search(r'<(.*)>',the_from).group(1)
                            # print from_address
                            # seed_email = msg.get('To', '')
                            # print email_address
                            send_time = USToLocaltime(msg.get('Date', ''))
                            # print send_time
                            if domain_name == 'sina.cn' or domain_name == 'sina.com' or domain_name == 'sohu.com':
                                sender = msg.get('X-Sender', '')
                                if "<" in sender:
                                    sender = re.search(r'<(.*)>',sender).group(1)
                            else:
                                sender = msg.get('Sender', '')
                            # print sender
                            # print "------------------------"
                            data = tuple([send_time, user_id, message_id, box_status, from_address, email_address, domain_name, sender, subject, num])
                            insertData(data)
                            # print data
                        else:
                            print "This mail %s doesn't sended from epcare!" % num
                            continue
                    except Exception, e:
                        print 'got msg error: %s' % e 
            M.close()
        M.logout()
    except Exception, e:
        print 'imap error:%s' % e 
        M.close()

if __name__ == '__main__':  
    datas = getSeedemail()
    for data in datas:
        email_address = data['email_address']
        domain_name = data['domain_name']
        pwd = data['password']
        parseMailHeader(email_address, domain_name, pwd)
    # parseMailHeader('jinghuahhh@sohu.com', 'sohu.com', 'qwer1234')