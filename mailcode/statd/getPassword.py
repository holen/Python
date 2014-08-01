#-* coding:UTF-8 -*
#!/usr/bin/env python

def getPassword():
    file_object = open('/root/bin/sewcloudpassword.txt', 'rb')
    try:
        password = file_object.read()
#        print password.strip("\r\n")
        return password.strip("\r\n")
    finally:
        file_object.close( )
