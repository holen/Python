#-* coding:UTF-8 -*
#!/usr/bin/env python
import thread

def run(n):
    for i in range(n):
        print i
        print "-------"

print thread.start_new_thread(run,(4,))

