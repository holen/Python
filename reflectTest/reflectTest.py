#!/usr/bin/env python

data = raw_input("input url: ")
array = data.split('/')

userspance = __import__('backend.'+array[0])
#userspance = __import__(array[0])
print type(userspance)

model = getattr(userspance, array[0])
print type(model)

#func = getattr(userspance, array[1])
func = getattr(model, array[1])
print type(func)

func()
