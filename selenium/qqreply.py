#!/usr/bin/env python3
#coding: utf-8

import sys
import time
import random
import qqcleanwhitelist as qqcl
import qqmovespam as qqmp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(1024, 768))
# display.start()


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
        print e
        sys.exit(0)

browser = webdriver.Firefox()
browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
browser.implicitly_wait(10)
username = sys.argv[1]
password = sys.argv[2]
reply_file = "/data/git/python/selenium/replycontent.txt"
login(username, password)

qqmp.movetoinbox(browser)

while True:
    try:
        # click inbox
        browser.find_element_by_css_selector('#folder_1').click()
        print "into inbox"
    except Exception, e:
        print e
        break

    # switch to mainFrame
    browser.switch_to_frame('mainFrame')

    # input
    try:
        input = browser.find_element_by_css_selector('input[unread=true]')
    except Exception, e:
        print "没有未读邮件"
        print e
        browser.refresh()
        qqcl.cleanwhitelist(browser)
        break
    # print input.get_attribute('unread')
    # print input.get_attribute('value')
    print "读取到一封未读邮件"
    fa = input.get_attribute('fa')
    domain = fa.split('@')[1]
    print domain
    if domain == "hechuangyi.com":
        # click mail
        browser.find_element_by_css_selector('span[mailid="%s"]' % input.get_attribute('value')).click()
        # time.sleep(1)

        # reply
        browser.find_element_by_id('tb_reply_all1').click()

        # input reply content
        # time.sleep(1)
        fclass = browser.find_element_by_css_selector(".qmEditorIfrmEditArea")
        fid = fclass.get_attribute('id')
        browser.switch_to_frame(fid)
        actions = ActionChains(browser)
        # actions.send_keys(reply_content)
        reply_content = random.choice(open(reply_file, 'rb').read().split('---'))
        actions.send_keys(reply_content.decode('utf8'))
        actions.key_down(Keys.CONTROL).key_down(Keys.ENTER).key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(2)
        print "reply content success"
    else:
        browser.find_element_by_css_selector('span[mailid="%s"]' % input.get_attribute('value')).click()
        time.sleep(1)
    browser.refresh()
    # time.sleep(2)

browser.quit()
# display.stop()
