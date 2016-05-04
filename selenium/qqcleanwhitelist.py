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


def cleanwhitelist(browser):
    # click setting
    # browser.find_element_by_css_selector('#frame_html_setting').click()
    browser.find_element_by_id('frame_html_setting').click()

    # switch to mainFrame
    browser.switch_to_frame('mainFrame')
    time.sleep(1)

    # click spam
    browser.find_element_by_partial_link_text("反垃圾").click()

    # click setting white_list
    browser.find_element_by_partial_link_text("设置邮件地址白名单").click()

    # clean white_list
    # browser.find_element_by_class_name("btn_gray").click()
    clean = browser.find_element_by_partial_link_text("清空全部白名单")
    clean.click()

    # submit
    clean.send_keys(Keys.ENTER)
    time.sleep(3)
    print "clean success"
    # Alert(browser).accept()
    # alert_window = browser.switch_to.alert
    # alert_window.dismiss()
    # try:
    #     driver.switch_to.alert.accept()
    # except NoAlertPresentException:
    #     pass

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
    browser.implicitly_wait(10)
    username = sys.argv[1]
    password = sys.argv[2]
    login(username, password)
    cleanwhitelist(browser)
