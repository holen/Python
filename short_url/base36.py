# _*_ encoding:utf-8 _*_
__author__ = 'zhl'
__date__ = '2019/10/15 18:08'


def base10_to_base36(number):
    alphabets = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    while number != 0:
        number, i = divmod(number, 36)
        result = (alphabets[i] + result)

    return result or alphabets[0]