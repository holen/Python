#-* coding:UTF-8 -*
#!/usr/bin/python

import argparse
parser = argparse.ArgumentParser(description="calculate X to the power of Y")
parser.add_argument("square", type=int, 
                    help="display a square of a given number")
parser.add_argument("-t", "--test", action="store_true")
#parser.add_argument("-v", "--verbosity", action="count", default=0,
#                    help="increase output verbosity")
group = parser.add_mutually_exclusive_group()
#group.add_argument("-v", "--verbosity", action="store_true")
group.add_argument("-v", "--verbosity", action="count", default=0.1,
                    help="increase output verbosity")
group.add_argument("-q", "--quiet", action="store_false")
args = parser.parse_args()
answer = args.square**2
print "false is %s" %  args.test
print "store_true is %s" % args.quiet
if args.verbosity >= 2:
    print "Running '{}'".format(__file__)
    print "the square of {} equals {}".format(args.square, answer)
elif args.verbosity >= 1:
    print "{}^2 == {}".format(args.square, answer)
else:
    print answer
    print args.verbosity
