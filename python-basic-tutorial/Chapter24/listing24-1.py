#-* coding:UTF-8 -*
#!/usr/bin/env python
from asyncore import dispatcher
import asyncore

class ChatServer(dispatcher): pass

s = ChatServer()
asyncore.loop()
