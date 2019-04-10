class A(object):
    a = 'a'

    @staticmethod
    def foo1(name):
        print("hello {}".format(name))

    def foo2(self, name):
        print("hello {}".format(name))

    @classmethod
    def foo3(cls, name):
        print("hello {}".format(name))


a = A()
a.foo1("foo1") # ('hello', 'foo1')
A.foo1("foo1") # ('hello', 'foo1')

a.foo2("foo2") # ('hello', 'foo2')
# A.foo2("foo2") # TypeError: unbound method foo2() must be called with A instance as first argument (got str instance instead)

a.foo3("foo3") # ('hello', 'foo3')
A.foo3("foo3") # ('hello', 'foo3')