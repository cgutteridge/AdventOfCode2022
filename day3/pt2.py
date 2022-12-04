#!/usr/bin/python3

import sys
from pprint import pprint

def priority(char):
    n = ord(thing)
    if( n < 97 ):
        n -= 65
        n += 26
    else:
        n -= 97
    n += 1
    return n

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'

with open(file, 'r') as f:
	lines = f.read().split("\n")

pt2 = 0;
for index in range(0, len(lines), 3 ):
    if ( lines[index] == "" ):
        continue
    chars1 = list( lines[index] )
    chars2 = list( lines[index+1] )
    chars3 = list( lines[index+2] )
    stuff1 = {}
    for i in range(0, len(chars1)):
        stuff1[chars1[i]] = 1
    stuff2 = {}
    for i in range(0, len(chars2)):
        stuff2[chars2[i]] = 1
    for i in range(0, len(chars3)):
        if( stuff1.get( chars3[i] ) != None and stuff2.get( chars3[i] ) != None):
            thing = chars3[i]
    pt2 += priority( thing )

        
print(f'PT2: {pt2}')

