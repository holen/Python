# coding: utf-8
import sys

def zigzag_encode(x):
    if x >= 0:
        return 2*x
    else:
        return -2 * x -1

def zigzag_decode(x):
    if x % 2 == 0:
        return x/2
    else:
        return -(x+1)/2

print "Please input a number: "
x = raw_input()

if sys.argv[1] == "encode":
    print zigzag_encode(int(x))
else:
    print zigzag_decode(int(x))
