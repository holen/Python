# -*- coding: utf-8 -*-


class Person(object):
    """Silly Person"""
    def __new__(cls, name, age):
        """__new__ 通常用于控制生成一个新实例的过程。它是类级别的方法"""
        print("in __new__")
        return object.__new__(cls)  # don't pass extra arguments here!

    def __init__(self, name, age):
        """__init__ 通常用于初始化一个新实例，控制这个初始化的过程，比如添加一些属性，
        做一些额外的操作，发生在类实例被创建完以后。它是实例级别的方法。"""
        print('__init__ called.')
        self.name = name
        self.age = age

    def __str__(self):
        return 'Person: {}({})'.format(self.name, self.age)


if __name__ == '__main__':
    piglei = Person('piglei', 24)
    print(piglei)

