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
        print e
        sys.exit(0)


logger = logging.getLogger()
handler = logging.FileHandler("/tmp/reply163.log")
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
logger.info(username)


def clickMail(box):
    num = 0
    while True:
        try:
            # click inbox
            inbox = browser.find_element_by_css_selector('span[title=%s]' % box)
            inbox.click()
            # print "into inbox"
            logger.info("into %s" % box)
        except Exception, e:
            # print e
            logger.error("into %s failed\n" % box)
            logger.error(e)
            break

        try:
            time.sleep(1)
            unread = browser.find_element_by_css_selector('b[title=未读]')
            # unread.click()
        except Exception, e:
            print "没有未读邮件"
            logger.info("没有未读邮件")
            logger.error(e)
            break

        try:
            mail = browser.find_element_by_id(unread.get_attribute('id').replace('LogoB', 'MidDiv'))
            mail.click()
            num += 1
            if num > 10:
                break
        except Exception, e:
            print "点击邮件错误"
            logger.info("点击邮件错误")
            logger.error(e)
            num += 1
            continue


def clickHideFolders():
    try:
        hideFolder = browser.find_element_by_id("spnHideFolders")
        hideFolder.click()
    except Exception, e:
        print "点击其他文件夹错误"
        logger.info("点击其他文件夹错误")
        logger.error(e)
        browser.quit()

clickMail("收件箱")
clickHideFolders()
clickMail("订阅邮件")
browser.quit()
