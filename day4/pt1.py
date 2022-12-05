#!/usr/bin/python3

import sys
from pprint import pprint

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'

with open(file, 'r') as f:
	lines = f.read().split("\n")
########################################3
pt1 = 0;

for line in lines:
    if ( line == "" ):
        continue
    elves = line.split( "," );
    elf1 = elves[0].split( "-" )
    elf2 = elves[1].split( "-" )
    elf1[0]=int(elf1[0])
    elf1[1]=int(elf1[1])
    elf2[0]=int(elf2[0])
    elf2[1]=int(elf2[1])
    if( (elf1[0]<=elf2[0] and elf1[1]>=elf2[1]) or ( elf2[0]<=elf1[0] and elf2[1]>=elf1[1] ) ):
        pt1+=1
    
        
print(f'PT1: {pt1}')
