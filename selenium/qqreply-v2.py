#!/usr/bin/env python3
#coding: utf-8

import sys
import time
import random
import logging
import qqmovespam as qqmp
from qqcleanwhitelist import cleanwhitelist
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()

username = sys.argv[1]
password = sys.argv[2]

logger = logging.getLogger()
handler = logging.FileHandler("/tmp/%s.log" % username.split('@')[0])
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# logger.setLevel(logging.NOTSET)
logger.setLevel(logging.INFO)


def login(login_name, passwd):
    '''login'''
    try:
        # # switch to login_frame
        browser.switch_to_frame('login_frame')

        username = browser.find_element_by_css_selector("#u")
        username.send_keys(login_name)
        time.sleep(1)
        password = browser.find_element_by_css_selector("#p")
        password.send_keys(passwd)
        # login_enable = browser.find_element_by_id("p_low_login_enable")
        # login_enable.click()
        password.send_keys(Keys.RETURN)
        time.sleep(2)
        #browser.find_element_by_id("login_button").click()
    except Exception, e:
        # print e
        logger.error("login failed\n: %s" % e)
        sys.exit(0)

browser = webdriver.Firefox()
browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
browser.implicitly_wait(10)
reply_file = "/root/replycontent.txt"
login(username, password)

qqmp.movetoinbox(browser)

while True:
    try:
        # click inbox
        browser.find_element_by_css_selector('#folder_1').click()
        # print "into inbox"
        logger.info("into inbox")
    except Exception, e:
        # print e
        logger.error("into inbox failed\n: %s" % e)
        break

    # switch to mainFrame
    browser.switch_to_frame('mainFrame')

    # input
    try:
        time.sleep(1)
        input = browser.find_element_by_css_selector('input[unread=true]')
    except Exception, e:
        # print "没有未读邮件"
        logger.info("没有未读邮件")
        # print e
        logger.error(e)
        # browser.refresh()
        # cleanwhitelist(browser)
        break
    # print input.get_attribute('unread')
    # print input.get_attribute('value')
    # print "读取到一封未读邮件"
    logger.info("读取到一封未读邮件")
    fa = input.get_attribute('fa')
    domain = fa.split('@')[1]
    # print domain
    logger.info(domain)
    if domain == "heyi.com":
        # click mail
        browser.find_element_by_css_selector('span[mailid="%s"]' % input.get_attribute('value')).click()
        time.sleep(1)

        # reply
        browser.find_element_by_id('tb_reply_all1').click()

        # input reply content
        time.sleep(1)
        try:
            fclass = browser.find_element_by_css_selector(".qmEditorIfrmEditArea")
        except Exception, e:
            logger.error("确认回复邮件框错误！ %s" % e)
            browser.quit()
            display.stop()
            sys.exit(0)
        fid = fclass.get_attribute('id')
        browser.switch_to_frame(fid)
        actions = ActionChains(browser)
        # actions.send_keys(reply_content)
        reply_content = random.choice(open(reply_file, 'rb').read().split('---'))
        actions.send_keys(reply_content.decode('utf8'))
        actions.key_down(Keys.CONTROL).key_down(Keys.ENTER).key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(3)
        print "reply content success"
        logger.info("reply content success")
    else:
        browser.find_element_by_css_selector('span[mailid="%s"]' % input.get_attribute('value')).click()
    time.sleep(1)
    browser.refresh()
    # time.sleep(2)

browser.quit()
display.stop()
