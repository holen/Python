#!/usr/bin/env python3
#coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('http://www.baidu.com')

browser.find_element_by_id("kw").send_keys('selenium')
browser.find_element_by_id("su").click()

browser.quit()
