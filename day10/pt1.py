#!/usr/bin/python3

import sys
from pprint import pprint

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")

cmds = []
for line in lines:
    if line=="": 
        continue
    args = line.split( " " )
    if( args[0] == "noop" ):
        cmds.append( 0 )
    if( args[0] == "addx" ):
        cmds.append( 0 )
        cmds.append( int(args[1]) )

# nb 0 index
x = 1
pt1 = 0
for i in range(0,len(cmds)):
    cycle = i+1
    if( (cycle-20)%40== 0 ):
        print(f'{cycle} .. {x}')
        pt1 += cycle*x
    x+=cmds[i]


print(f'PT1: {pt1}')

