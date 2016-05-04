#!/usr/bin/env python3
#coding: utf-8

import sys
import time
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

browser = webdriver.Firefox()
browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
# addcookie()
# browser.get("https://mail.qq.com/cgi-bin/loginpage?lang=cn")
username = sys.argv[1]
passwd = sys.argv[2]

login(username, passwd)

# click setting
browser.find_element_by_css_selector('#frame_html_setting').click()

# switch to mainFrame
browser.switch_to_frame('mainFrame')

# set lang cn
lang = browser.find_element_by_css_selector("span[class=btn_select_txt]")
lang.click()
#print lang.text.encode('utf-8')
cnlan = browser.find_element_by_id("select_QMMenu__menuitem_cn")
cnlan.click()

# set page show count
showcountContainer = browser.find_element_by_id("showcountContainer")
showcount = showcountContainer.find_element_by_tag_name('a')
#id = showcount.get_attribute('id')
showcount.click()
count50 = browser.find_element_by_id("select_QMMenu__menuitem_2")
count50.click()

# ad
advertsyn = browser.find_element_by_id("openadvertsyn")
flag = advertsyn.is_selected()
if flag:
    advertsyn.click()

# radio
browser.find_element_by_css_selector('input[id=delflag1]').click()

# save setting
save = browser.find_element_by_id("sendbtn")
save.click()

# click inbox
# browser.find_element_by_css_selector('#folder_1').click()

# browser.quit()
