#!/usr/bin/python

import sys

def main(argv):
    (last_word, sum) = (None, 0)

    # input comes from STDIN
    for line in sys.stdin:
        # parse the input we got from mapper.py
        (cur_word, value) = line.strip().split('\t')
        
        if last_word and last_word != cur_word:
            # write result to STDOUT
            print last_word + '\t' + str(sum)
            (last_word, sum) = (cur_word, int(value))
        else:
            (last_word, sum) = (cur_word, sum + int(value))

    if last_word:
        print last_word + '\t' + str(sum)


if __name__ == "__main__":
    main(sys.argv)
