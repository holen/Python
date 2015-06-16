
def deco(f):
    print "ha ha ha "
    #f()
    #print "I am finished ..."
    return f

@deco
def sayHi():
    print "I am zhl"

print type(sayHi)
print type(sayHi())
sayHi()

print " ------------ "

def dico(f):
    print "ha ha ha "

@dico
def sayHe():
    print "I am zhl"

print type(sayHe)
sayHe

print " ********* "

def dece(f):
    def pack(*args, **kwargs):
        print "I am in pack "
        f(*args, **kwargs)
        print "I am finished ... welcome", args, kwargs
    return pack

@dece
def sayHa(name, age):
    print "I am %s, i am %s years old .... " % (name, age)

sayHa("zhl", 26)

