import urllib2
from BeautifulSoup import BeautifulSoup

def get_result(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
	results = soup.findAll('font', {"color":"red"})
	for result in results:
		print result

for i in range(2, 255):
	url='''http://www.spamhaus.org/query/ip/36.248.236.%s'''
	link = url % (i)
	get_result(link)
