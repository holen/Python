#-* coding:UTF-8 -*
#!/usr/bin/env python

from xml.sax.handler import ContentHandler
from xml.sax import parse

class TestHandler(ContentHandler):
    def startElement(self, name, attrs):
        print name, attrs.keys()
        for key, val in attrs.items():
             print ' %s="%s"' % (key, val)

parse('website.xml', TestHandler())


