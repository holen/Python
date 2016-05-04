#!/usr/bin/env python3
#coding: utf-8

import time
from selenium import webdriver

dr = webdriver.Firefox()

url = 'http://www.baidu.com'
dr.get(url)

dr.add_cookie({'name': 'BAIDUID', 'value': 'xxxxxxxxxxxxxxx', 'path': '/'})
dr.add_cookie({'name': 'BDUSS', 'value': 'xxxxxxxxxxxxxxxxx', 'path': '/'})

dr.get(url)

time.sleep(10)

dr.quit()
