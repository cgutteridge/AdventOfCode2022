#!/usr/bin/python3

import sys
from pprint import pprint

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'

with open(file, 'r') as f:
	lines = f.read().split("\n")

########################################

def distinct(values):
    seen = {}
    for value in values:
        if( seen.get(value) != None ):
            return False
        seen[value]=1
    return True

########################################

# test mode has multiple lines
for line in lines:
    if line=="":
        continue
    # find marker
    # loop over 4 char sets, finding first that's all unique
    chars = list(line)
    blocksize = 14
    for i in range(0,len(chars)-(blocksize-1)):
        mark = chars[i:i+blocksize];
        if( distinct(mark) ):
            pt2=i+blocksize
            print(f'PT2: {pt2}')
            break


