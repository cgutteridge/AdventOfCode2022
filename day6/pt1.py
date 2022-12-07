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
    for i in range(0,len(chars)-3):
        mark = chars[i:i+4];
        if( distinct(mark) ):
            pt1=i+4
            print(f'PT1: {pt1}')
            break


