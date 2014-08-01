#-* coding:UTF-8 -*
#!/usr/bin/env python

from time import strftime
from time import time, localtime

day = 24 * 60 * 60
print day
# 86400
yesterday = localtime(time() - day)
print yesterday
# time.struct_time(tm_year=2014, tm_mon=5, tm_mday=20, tm_hour=15, tm_min=33, tm_sec=13, tm_wday=1, tm_yday=140, tm_isdst=0)
print strftime('%y%m%d')
# '140521'
print strftime('%H%M%S')
# '153358'
date = strftime('%y%m%d', yesterday)
hour = strftime('%H%M%S', yesterday)
