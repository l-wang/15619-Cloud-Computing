#!/usr/bin/python
import os
import sys
import re
import gzip


ins = open( "output", "r" )
max = 0

for line in ins:
	split_result = line.strip().split('\t')
	val = int(split_result[1])
	print val
	if val > max:
		max = val

print max
