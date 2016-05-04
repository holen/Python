#!/usr/bin/python
#coding: utf-8
import smtplib
import socket
import argparse
import re
import shlex
import subprocess
import sys
import time
import dkim
import urllib2
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.header import Header

logger = logging.getLogger()
handler = logging.FileHandler("/tmp/sendmail.log")
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class mySMTP(smtplib.SMTP):
    def _get_socket(self, host, port, timeout):
        if self.debuglevel > 0:
            print>>stderr, 'connect:', (host, port)
        return socket.create_connection((host, port), timeout, source_address)


def digmx(to_mail, source_ip):
    domain = re.split('@', to_mail)[1]
    cmd = "dig -b %s %s mx +short @114.114.114.114"
    args = shlex.split(cmd % (source_ip, domain))
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        out = p.stdout.readlines()
        mx = out[0].split(" ")[1].strip(".\n")
        return mx
    except Exception, e:
        print e
        sys.exit()


def startsend(smtp_server, smtp_server_port, source_address, from_name, mail_from, to_mail, subject, html):
    real_from = re.split('@', mail_from)[1]
    try:
        server = mySMTP(smtp_server, smtp_server_port, real_from, 30)
    except Exception, e:
        print e
        sys.exit()
    server.set_debuglevel(0)
    # server.set_debuglevel(1)
    # server.docmd('helo', real_from)
    # server.docmd('mail from:<%s>' % mail_from)
    # server.docmd('rcpt to:<%s>' % to_mail)
    msg = MIMEText(html, 'html', 'UTF-8')
    # sig = dkim.sign(msg.as_string(), "default", real_from, open("/etc/opendkim/keys/hechuangyi.com/default.private").read())
    # msg['DKIM-Signature'] = sig[16:]
    msg["From"] = '"%s" <%s>' % (Header(from_name, 'utf-8'), mail_from)
    msg["To"] = to_mail
    msg['Subject'] = Header(subject, 'utf-8')
    msg['Date'] = formatdate(localtime=True)
    try:
        server.sendmail(mail_from, to_mail, msg.as_string())
        print "%s send Ok" % to_mail
	logging.info("%s send Ok" % to_mail)
    except smtplib.SMTPRecipientsRefused, e:
        print "recipient addresses refused."
        print to_mail, e
	logging.debug("recipient addresses refused. %s, %s" % (to_mail, e))
    except smtplib.SMTPDataError, e:
        print "The SMTP server refused to accept the message data"
        print to_mail, e
	logging.debug("The SMTP server refused to accept the message data. %s, %s" % (to_mail, e))
    except smtplib.SMTPHeloError, e:
        print "The server didn’t reply properly to the HELO greeting"
        print to_mail, e
	logging.debug("The server didn’t reply properly to the HELO greeting. %s, %s" % (to_mail, e))
    except smtplib.SMTPSenderRefused, e:
        print "The server didn’t accept the from_addr."
        print to_mail, e
	logging.debug("The server didn’t accept the from_addr. %s, %s" % (to_mail, e))
    except Exception, e:
        print to_mail, e
	logging.debug("Exception. %s, %s" % (to_mail, e))
    server.quit()
    time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Send mail use specified args")
    parser.add_argument("-m", "--mail_from", required=True, action="store", dest='mail_from', help="sender")
    parser.add_argument("-n", "--from_name", required=True, action="store", dest='from_name', help="sender name")
    parser.add_argument("-t", "--to_mail", required=True, action="store", dest='to_mail', help="receiver")
    parser.add_argument("-i", "--source_ip", required=True, action="store", dest='source_ip', help="specified local send ip")
    parser.add_argument("-S", "--smtp_server", action="store", dest='smtp_server', help="The remote smtp server")
    parser.add_argument("-p", "--port", action="store", type=int, dest='smtp_server_port', help="remote smtp server port")
    parser.add_argument("-r", "--real_from", action="store", dest='real_from', help="The real from domain")
    parser.add_argument("-s", "--subject", required=True, action="store", dest='subject', help="mail subject")
    parser.add_argument("-c", "--content", action="store", dest='content', help="mail content")
    parser.add_argument("-f", "--file", action="store", dest='content_file', help="mail html content file")
    parser.add_argument("-u", "--url", action="store", dest='url', help="get mail content from url")

    args = parser.parse_args()
    mail_from = args.mail_from
    from_name = args.from_name
    to_mail = args.to_mail
    source_ip = args.source_ip
    global source_address
    source_address = (source_ip, 0)
    # html
    html_template = """
    <html>
        <head></head>
        <body>
            <p>%s<p>
        </body>
    </html>
    """
    if args.smtp_server:
        smtp_server = args.smtp_server
    else:
        smtp_server = digmx(to_mail, source_ip)
    if args.smtp_server_port:
        smtp_server_port = args.smtp_server_port
    else:
        smtp_server_port = 25
    subject = args.subject
    if args.content:
        content = args.content
        html = html_template % content
    if args.content_file:
        content = open(args.content_file, 'rb').read()
        # content.decode('utf-8')
        html = content
    if args.url:
        httpResponse = urllib2.urlopen(args.url)
        html = httpResponse.read()
    startsend(smtp_server, smtp_server_port, source_address, from_name, mail_from, to_mail, subject, html)
