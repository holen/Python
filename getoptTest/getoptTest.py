#-* coding:UTF-8 -*
#!/usr/bin/env python
import getopt, sys

def usage():
    print("Usage:%s [-h|o|-v] [--help|--output] args...." % sys.argv[0]);

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    print opts 
    print args
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
            print "Version: 1.0 " 
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    # ...

if __name__ == "__main__":
    main()
