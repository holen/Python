#!/usr/bin/python

import sys
import email
import string
import imaplib


def loginIMAP(email_address, passwd):
    """Login the imap base on ssl"""
    M = imaplib.IMAP4_SSL("imap.qq.com")
    try:
        M.login(email_address, passwd)
        return M
    except Exception, e:
        print 'login error:%s' % e
        M.close()
        sys.exit(1)


def checkspam(email_address, pwd='qwer1234'):
    """Get spam email ..."""
    M = loginIMAP(email_address, pwd)
    # box_array = ['INBOX', 'Junk']
    box_array = ['Junk']
    uid_list = []
    for box in box_array:
        result, messages = M.select(box)
        if result != "OK":
            print "select result failed, error: %s" % result
        result, data = M.uid('search', None, 'ALL')
        if result != "OK":
            print "search result failed, error: %s" % result
        if not data[0]:
            continue
        for uid in string.split(data[0]):
            typ, data = M.uid('fetch', uid, '(RFC822.HEADER)')
            if result != "OK":
                print "fetch result failed, error: %s" % result
            try:
                msg = email.message_from_string(data[0][1])
                sender = msg.get('X-QQ-ORGSender')
                domain_name = sender.split('@')[1]
                if domain_name == 'hechuangyi.com':
                    uid_list.append(uid)
                # print "message: %s sender: %s in %s" % (uid, sender, box)
            except Exception, e:
                print 'get msg info error: %s' % e
    return uid_list
    M.close()
    M.logout()

if __name__ == '__main__':
    email_address = 'wahaha_2015@qq.com'
    passwd = 'awdzgcpzqzmjeach'
    uid_list = checkspam(email_address, passwd)
    print uid_list
