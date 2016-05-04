from selenium import webdriver

proxy_ip = '121.41.34.223'
proxy_port = '10086'
profile = webdriver.FirefoxProfile()
# Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", proxy_ip)
profile.set_preference("network.proxy.socks_port", int(proxy_port))
profile.update_preferences()

driver = webdriver.Firefox(firefox_profile=profile)

driver.get("http://ip138.com/")
