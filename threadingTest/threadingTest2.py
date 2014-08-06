#-* coding:UTF-8 -*
#!/usr/bin/env python
import threading

def run(x, y):
    for i in range(x, y):
        print i

t1 = threading.Thread(target=run, args=(15,20))

t1.start()
