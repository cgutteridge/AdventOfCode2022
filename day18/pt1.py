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

d = {}
for line in lines:
    if line == "":
        continue
    d[line]=True

pt1 = 0
dirs = [
        [0,0,1],
        [0,0,-1],
        [0,1,0],
        [0,-1,0],
        [1,0,0],
        [-1,0,0]]
for line in lines:
    if line == "":
        continue
    xyz_s = line.split( "," )
    x = int(xyz_s[0])
    y = int(xyz_s[1])
    z = int(xyz_s[2])
    
    for off in dirs:
        adjcode = f'{x+off[0]},{y+off[1]},{z+off[2]}'
        if not adjcode in d:
            pt1+=1


print( f'PART 1 = {pt1}' )

