class A(object):
    a = 'a'

    @staticmethod
    def foo1(name):
        print('hello {}'.format(name))
        print(A.a)
        # print(A.foo2("foo2")) # TypeError: unbound method foo2() must be called with A instance as first argument (got str instance instead)
        print("foo1 end")

    def foo2(self, name):
        print('hello {}'.format(name))

    @classmethod
    def foo3(cls, name):
        print('hello {}'.format(name))
        print(A.a)
        print(cls().foo2("foo2"))


a = A()
a.foo1("foo1")
# hello foo1
# a
a.foo3("foo3")
# hello foo3
# a
# hello foo2
# None