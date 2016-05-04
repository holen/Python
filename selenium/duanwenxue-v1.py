#!/usr/bin/env python2.7
# coding: utf-8
import os
import re
import sys
import logging
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger()
handler = logging.FileHandler("/tmp/duanwen.log")
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def getDomain(url):
    parsed_uri = urlparse(url)
    website = '{uri.netloc}'.format(uri=parsed_uri)
    return website


def parsehtml(url):
    try:
        httpResponse = urllib2.urlopen(url)
    except Exception, e:
        logger.error("Error: Access url error! %s %s " % (url, e))
        return False
    if httpResponse.code == 200 or httpResponse.code == 301 or httpResponse.code == 302:
        html = httpResponse.read()
        try:
            soup = BeautifulSoup(html, from_encoding="gb18030")
            return soup
        except Exception, e:
            logger.error("Error: soup html failed %s %s " % (url, e))
            return False
    else:
        logger.error("Error: httpResponse code %s " % (httpResponse.code))
        return False

piper_url = sys.argv[1]
soup = parsehtml(piper_url)
website = getDomain(piper_url)
try:
    # pageurls = soup.find_all("li", href=True)
    pageurls = soup.find_all("a", href=True)
except Exception, e:
    logger.error("Error: get href failed %s %s " % (piper_url, e))
    sys.exit(0)
# print pageurls[75]
# print pageurls[75].get('href')
# print pageurls[75].get_text()
url_list = []
if pageurls:
    for link in pageurls:
        sublink_href = link.get("href")
        p = re.compile(r'(article/)')
        match = p.search(sublink_href)
        if match:
            url_list.append("http://%s%s" % (website, sublink_href))

# url_list = ["http://www.duanwenxue.com/article/725546.html"]
head_html = "<html><head><title>duanwen</title></head><body>"
end_html = "</body></html>"

for url in url_list:
    # print url
    file_name = os.path.splitext(url.split('/')[-1])[0]
    soup1 = parsehtml(url)
    h1 = soup1.find_all("h1")
    title = h1[0].get_text()
    p_list = soup1.find_all("p")
    # print type(h1[0])
    html_file = file_name + ".html"
    fp = open(html_file, 'wb+')
    fp.write(head_html+'\n')
    fp.write('<h1 style="text-align:center">'+'\n')
    fp.write(title.encode('utf8')+'\n')
    fp.write('</h1>'+'\n')
    print '''%s=>wenxue/%s''' % (title.strip().encode('utf8'), html_file)
    for p in p_list:
        # print p.parent['class'][0]
        if p.parent['class'][0] == "article-content":
            if p.get_text().find(u"版权作品") == -1 and p.get_text().find('qq:') == -1:
                fp.write('<p>'+'\n')
                fp.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+p.get_text().encode('utf8')+'\n')
                fp.write("</p>"+"\n")
    fp.write(end_html)
    fp.close()
