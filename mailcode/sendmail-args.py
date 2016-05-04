#!/usr/bin/python
import base64
import smtplib
import socket
import argparse
import re
import shlex, subprocess
import sys
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.utils import COMMASPACE,formatdate
from email.header import Header 

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
        p = subprocess.Popen(args,stdout=subprocess.PIPE)
        out = p.stdout.readlines()
        mx = out[0].split(" ")[1].strip(".\n")
    except Exception,e:
        print e
        sys.exit()
    return mx

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Send mail use specified args")
parser.add_argument("-m", "--mail_from", required=True, action="store", dest='mail_from', help="sender")
parser.add_argument("-t", "--to_mail", required=True, action="store", dest='to_mail', help="receiver")
parser.add_argument("-i", "--source_ip", required=True, action="store", dest='source_ip', help="specified local send ip")
parser.add_argument("-S", "--smtp_server", action="store", dest='smtp_server', help="The remote smtp server")
parser.add_argument("-p", "--port", action="store", type=int, dest='smtp_server_port', help="remote smtp server port")
parser.add_argument("-r", "--real_from", action="store", dest='real_from', help="The real from domain")
parser.add_argument("-s", "--subject", required=True, action="store", dest='subject', help="mail subject")
parser.add_argument("-c", "--content", action="store", dest='content', help="mail content")
parser.add_argument("-f", "--file", action="store", dest='content_file', help="mail content file")

args = parser.parse_args()
mail_from = args.mail_from
from_user = mail_from.split('@')[0]
to_mail = args.to_mail
to_user = to_mail.split('@')[0]
source_ip = args.source_ip
source_address = (source_ip, 0)

if args.smtp_server:
    smtp_server = args.smtp_server
else:
    smtp_server = digmx(to_mail, source_ip)
if args.smtp_server_port:
    smtp_server_port = args.smtp_server_port
else:
    smtp_server_port = 25
if args.real_from:
    real_from = args.real_from
else:
    real_from = re.split('@', mail_from)[1]
subject = args.subject
# subject_base64 = base64.encodestring(subject).strip()
# subject = "=?UTF-8?B?%s?=" % subject_base64
if args.content:
    content = args.content
if args.content_file:
    content = open(args.content_file, 'rb').read()
    content.decode('utf-8')
server=mySMTP(smtp_server, smtp_server_port, real_from, 30)
server.set_debuglevel(1)
server.docmd('helo', real_from)
server.docmd('mail from:<%s>' % mail_from)
server.docmd('rcpt to:<%s>' % to_mail)
#msg = """from: %s <%s>
#to: %s <%s>
#subject: %s
#MIME-Version: 1.0
#Content-Type: text/html;charset=utf-8
#Content-Transfer-Encoding: quoted-printable
#
#%s
#"""
msg = MIMEMultipart()
# msg = MIMEText()
# from, to, subject
msg["From"] = mail_from
msg["To"] = to_mail
# msg['Subject'] = subject
msg['Subject'] = Header(subject, 'utf-8')   
msg['Date'] = formatdate(localtime=True)
# html
html = """
<html>
	<head></head>
	<body>
		<p>%s<p>
	</body>
</html>
"""
content = MIMEText(html % content, 'html', 'UTF-8')
msg.attach(content)
# server.sendmail(mail_from, to_mail, msg % (from_user, mail_from, to_user, to_mail, subject, content))
server.sendmail(mail_from, to_mail, msg.as_string())
server.quit()
