#!/usr/bin/env python

import sys

def main() : 

    for line in sys.stdin:

        output = line.strip()

        #print >> sys.stderr, output
        print >> sys.stdout, output

if  __name__ == "__main__" :
    main()

