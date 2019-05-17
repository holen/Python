# C 
from cStringIO import StringIO
# python
# from StringIO import StringIO

s = StringIO()
s.write("hello, ireader")
s.seek(0)
print s.read(1024)
