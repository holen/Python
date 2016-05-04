#!/usr/bin/env python3
#coding: utf-8

import sys
import time
import logging
from selenium import webdriver


def login(login_name, passwd):
    '''login'''
    try:
        username = browser.find_element_by_id("idInput")
        username.send_keys(login_name)
        password = browser.find_element_by_id("pwdInput")
        password.send_keys(passwd)
        browser.find_element_by_id("loginBtn").click()
        time.sleep(1)
    except Exception, e:
        # print e
        browser.quit()
        sys.exit(0)


logger = logging.getLogger()
handler = logging.FileHandler("/tmp/check163mail.log")
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# logger.setLevel(logging.NOTSET)
logger.setLevel(logging.INFO)
browser = webdriver.Firefox()
browser.implicitly_wait(10)
browser.get("http://mail.163.com/")

username = sys.argv[1]
passwd = sys.argv[2]

login(username, passwd)

try:
    # click inbox
    inbox = browser.find_element_by_css_selector('span[title=收件箱]')
    inbox.click()
    # print "into inbox"
    print "username: %s passwd: %s is_Ok" % (username, passwd)
    logger.info("username: %s passwd: %s is_Ok" % (username, passwd))
    browser.quit()
except Exception, e:
    print "username: %s passwd: %s Wrong" % (username, passwd)
    logger.error("username: %s passwd: %s Wrong" % (username, passwd))
    browser.quit()
