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

pt1 = 0;

for line in lines:
    if ( line == "" ):
        continue
    chars = list( line )
    size = int(len( chars ) / 2)
    stuff = {}
    for i in range(0, size):
        stuff[chars[i]] = 1
    thing = ""
    for i in range(size,size*2):
        if( stuff.get( chars[i] ) != None ):
            thing = chars[i]
            break

    pt1 += priority( thing )
    
        
print(f'PT1: {pt1}')


#	if( line == "" ):
#		if( current_elf != -1 ):
#			elves.append( current_elf )
#		current_elf = 0
#		continue
#	current_elf += int(line)
#
#max_elf = 0
#for elf in elves:
#    if( elf > max_elf ):
#        max_elf=elf
#
#
#elves.sort(reverse=True)
#
#top3 = elves[0]+elves[1]+elves[2]
#
#print(f'PT2: {top3}')
