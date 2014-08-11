#-* coding:UTF-8 -*
#!/usr/bin/env python
import urllib2
import cookielib

def HandleCookie():
    #handle cookie whit file
    filename='FileCookieJar.txt'
    url='http://www.baidu.com'
    FileCookieJar=cookielib.LWPCookieJar(filename)
    FileCookieJar.save()
    opener =urllib2.build_opener(urllib2.HTTPCookieProcessor(FileCookieJar))
    opener.open(url)
    FileCookieJar.save()
    print open(filename).read()

    #read cookie from file
    readfilename = "readFileCookieJar.txt"
    MozillaCookieJarFile =cookielib.MozillaCookieJar()
    print "MozillaCokieJarFIle is %s " % MozillaCookieJarFile       
    MozillaCookieJarFile.save(readfilename)
    MozillaCookieJarFile.load(readfilename)
    print "load Mozilla is %s " % MozillaCookieJarFile
if __name__=="__main__":
    HandleCookie()
