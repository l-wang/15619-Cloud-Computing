#!/usr/bin/python

import os
import sys
import re

def main(argv):
    (last, sum) = (None, 0)

    # input comes from STDIN
    for line in sys.stdin:
        # parse the input we got from mapper.py
        (cur, value) = line.strip().split('\t')
        
        if last and last != cur:
            # write result to STDOUT
            print last + '\t' + str(sum)
            (last, sum) = (cur, int(value))
        else:
            (last, sum) = (cur, sum + int(value))

    if last and sum>=100000,:
        print last + '\t' + str(sum)


if __name__ == "__main__":
    main(sys.argv)