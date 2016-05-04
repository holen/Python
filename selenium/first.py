#!/usr/bin/env python3
# coding: utf-8
# pip2.7 install selenium
# yum -y install firefox
# pip2.7 install pyvirtualdisplay
# yum -y insatll xorg-x11-server-Xvfb
# yum install wqy-microhei-fonts

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(1024, 768))
# display.start()


browser = webdriver.Firefox()

browser.get('http://www.baidu.com')
print browser.title.encode('utf-8')

browser.find_element_by_id("kw").send_keys('selenium')
browser.find_element_by_id("su").click()

print dir(browser)
print browser.current_url
print browser.current_window_handle
print browser.window_handles

# browser.get_screenshot_as_file("/tmp/baidu.png")
browser.save_screenshot("/tmp/1.png")

browser.quit()
# display.stop()
