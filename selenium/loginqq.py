#!/usr/bin/env python3
#coding: utf-8

import os
import sys
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
        login_enable = browser.find_element_by_id("p_low_login_enable")
        login_enable.click()
        password.send_keys(Keys.RETURN)
        time.sleep(2)
        #browser.find_element_by_id("login_button").click()
    except Exception, e:
        print e
        sys.exit(0)


def save_cookie():
    pickle.dump(browser.get_cookies(), open("/tmp/cookies.pkl", "wb"))


def addcookie():
    cookies = pickle.load(open("/tmp/cookies.pkl", "rb"))
    for cookie in cookies:
        cookie.pop('httpOnly')
        cookie.pop('domain')
        browser.add_cookie(cookie)

browser = webdriver.Firefox()
browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
# addcookie()
# browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
username = '15@qq.com'
passwd = '15'

login()
save_cookie()

browser.quit()
