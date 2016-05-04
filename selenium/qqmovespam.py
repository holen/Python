#!/usr/bin/env python3
#coding: utf-8

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import *


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


def movetoinbox(browser):
    try:
        # click inbox
        spam = browser.find_element_by_css_selector('#folder_6')
        spam.click()

        print "into spam"
        # switch to mainFrame
        browser.switch_to_frame('mainFrame')

        # select all spam
        browser.find_element_by_id('ckb_selectAll').click()

        # click move
        browser.find_element_by_partial_link_text("移动到...").click()

        # click move to inbox
        browser.find_element_by_id('select_QMMenu__menuitem_fid_1').click()
        time.sleep(3)
        print "move to inbox sucess"
        browser.refresh()
    except Exception, e:
        browser.refresh()
        print e
        return


if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
    browser.implicitly_wait(10)
    username = sys.argv[1]
    password = sys.argv[2]
    login(username, password)
    movetoinbox(browser)
    browser.quit()
