#-* coding:UTF-8 -*
#!/usr/bin/env python

while True:
    flag = raw_input("There are affect %s rows on messages:%s and last_rt_id=%s, are you when to continue [y/n]:")
    if flag == 'y':
        print "y"
        break
    elif flag == 'n':
        print "Nothing is dode !"
        break
    else:                                                                                               
        print "Please input y/n "
