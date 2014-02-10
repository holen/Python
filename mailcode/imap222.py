import imaplib
import string, random
import StringIO, rfc822

server = 'imap.sina.com'

user = 'xmepcare0006@sina.com'
password = 'qwer1234'

m = imaplib.IMAP4('imap.sina.com')

m.login(user,password)
m.select()

resp, items = server.search(None, "ALL")
items = string.split(items[0])