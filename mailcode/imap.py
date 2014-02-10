import imaplib, string, email
from email.parser import Parser

M = imaplib.IMAP4("imap.163.com")

try:
	try:
		M.login('yh_zhl@163.com','yhqwer1234')
	except Exception, e:
		print 'login error:%s' %e
		M.close()
	M.select()
	result, message = M.select()
	typ, data = M.search(None, '(AFTER "9-Jun-2013")')
	print data
	for num in string.split(data[0]):
		try:
			typ,data = M.fetch(num, '(RFC822)')
			msg = email.message_from_string(data[0][1])
			print msg
			headers = Parser().parsertr(msg)
			print headers['from']
			# print msg["From"]
			# print msg["Subject"]
			# print msg["Date"]
			# print "------------------------"
		except Exception, e:
			print 'got msg error: %s' % e 
	# typ,data = M.fetch(30, '(RFC822)')
	# print data
	# msg = email.message_from_string(data[0][1])
	# print msg["From"]
	# print msg["Subject"]
	# print msg["Date"]
	M.close()
	M.logout()
except Exception, e:
	print 'imap error:%s' % e 
	M.close()