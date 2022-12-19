#!/usr/bin/python3

import sys
import re
import copy
from pprint import pprint,pformat

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
    y = 10
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")

for line in lines:
    if line == "":
        continue
    #stuff



answer = -1

print( f'PART 1 = {answer}' )

