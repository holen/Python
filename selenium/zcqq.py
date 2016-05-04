#!/usr/bin/env python3
#coding: utf-8

from PIL import Image
from selenium import webdriver

# proxy setting
# proxy_ip = '121.41.34.223'
# proxy_port = '10086'
# profile = webdriver.FirefoxProfile()
# # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.socks", proxy_ip)
# profile.set_preference("network.proxy.socks_port", int(proxy_port))
# profile.update_preferences()
# driver = webdriver.Firefox(firefox_profile=profile)

driver = webdriver.Firefox()
driver.get('http://zc.qq.com/en/index.html')

driver.find_element_by_css_selector("#other_email").click()
driver.find_element_by_id("no_email").click()
# driver.find_element_by_id("email_info").click()

# username
username = driver.find_element_by_id("self_email")
username.send_keys("wahaha_2015_1")

# nick
nick = driver.find_element_by_id("nick")
nick.send_keys("wahaha")

# password
pwd = driver.find_element_by_id("password")
pwd.send_keys("wahaha")
pwd2 = driver.find_element_by_id("password_again")
pwd2.send_keys("wahaha")

# year mon day
driver.find_element_by_id("year_value").click()
driver.find_element_by_id("month_value").click()
driver.find_element_by_id("day_value").click()

# country province city
driver.find_element_by_id("country_value").click()
driver.find_element_by_id("province_value").click()
driver.find_element_by_id("city_value").click()
driver.find_element_by_id("code").click()

# capture current window
driver.save_screenshot('/tmp/code_img.png')

# code
img = driver.find_element_by_css_selector("#code_img")
# js_context = '''
#     var img = arguments[0];
#     if (!!((img.complete && typeof img.naturalWidth !== "undefined") || img.width)) {
#         var canvas = document.createElement('canvas');
#         canvas.width = img.width;
#         canvas.height = img.height;
#         canvas.getContext('2d').drawImage(img, 0, 0);
#         dataURL = canvas.toDataURL("image/png");
#         return dataURL;
#     }
# '''
# # return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
# dataURL = driver.execute_script(js_context, img)
# print dataURL

# draw code img
js_left = '''
    element = arguments[0];
　　　　var actualLeft = element.offsetLeft;
　　　　var current = element.offsetParent;
　　　　while (current !== null){
　　　　　　actualLeft += current.offsetLeft;
　　　　　　current = current.offsetParent;
　　　　}
　　　　return actualLeft;
'''
js_top = '''
    element = arguments[0];
　　　　var actualTop = element.offsetTop;
　　　　var current = element.offsetParent;
　　　　while (current !== null){
　　　　　　actualTop += current.offsetTop;
　　　　　　current = current.offsetParent;
　　　　}
　　　　return actualTop;
'''
left = int(driver.execute_script(js_left, img))
top = int(driver.execute_script(js_top, img))
right = left + int(img.get_attribute("width"))
bottom = top + int(img.get_attribute("height"))
# print left, top, right, bottom
im = Image.open('/tmp/code_img.png')
im = im.crop((left, top, right, bottom))
im.save('/tmp/code.png')
