#-* coding:UTF-8 -*
#!/usr/bin/env python
import threading
import time
import sys

class mythread(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        time.sleep(5)
        print self.id

t = mythread(1)

def func():
    t.start()
    print t.isAlive()

func()
sys.exit()
