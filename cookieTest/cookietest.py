#-* coding:UTF-8 -*
#!/usr/bin/env python

import os
print "Content-type: text/plain\n"
if "HTTP_COOKIE" in os.environ:
    print os.environ["HTTP_COOKIE"]
else:
    print "HTTP_COOKIE not set!"

