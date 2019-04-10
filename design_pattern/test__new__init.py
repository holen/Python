# -*- coding: utf-8 -*-


class Person(object):
    """Silly Person"""
    def __new__(cls, name, age):
        print("in __new__")
        return object.__new__(cls)  # don't pass extra arguments here!

    def __init__(self, name, age):
        print('__init__ called.')
        self.name = name
        self.age = age

    def __str__(self):
        return 'Person: {}({})'.format(self.name, self.age)


if __name__ == '__main__':
    piglei = Person('piglei', 24)
    print(piglei)

