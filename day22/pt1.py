#!/usr/bin/python3

import sys
import re
import copy
from pprint import pprint,pformat

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")
i=0
map = []
while lines[i]!="":
    row = []
    for j in range(0,len(lines[i])):
        row.append(lines[i][j])
    map.append(row)
    i += 1
plan = []
pstr = lines[i+1]+"X"
num = ""
for j in range(0,len(pstr)):
    c = pstr[j]
    if c>="0" and c<="9":
        num+=c
        continue
    plan.append( ['move',int(num)] )
    num = ""
    if c=="R":
        plan.append( ['turn',1] )
    if c=="L":
        plan.append( ['turn',-1] )
pprint(plan)


dirs = [ [1,0], [0,1], [-1,0], [0,-1] ]
icon = ">v<^"

facing = 0
y = 0
x = 0
while map[y][x]==" ":
    x+=1

def get_step(map,x,y,facing):
    xi = x+dirs[facing][0]
    yi = y+dirs[facing][1]
    wrap = False
    if yi>=0 and yi<len(map) and xi>=0 and xi<len(map[yi]) and map[yi][xi]!=" ":
        return [xi,yi]

    print(f'WRAP! {x},{y} {icon[facing]} ')

    rev = (facing+2)%4
    xwrap = x
    ywrap = y
    xi = xwrap + dirs[rev][0]
    yi = ywrap + dirs[rev][1]
    while yi>=0 and yi<len(map) and xi>=0 and xi<len(map[yi]) and map[yi][xi]!=" ":
        xwrap = xi
        ywrap = yi
        xi += dirs[rev][0]
        yi += dirs[rev][1]
    return [ xwrap,ywrap ]

pmap=False
for task in plan:
    if pmap:
        print()
        for yi in range(0,len(map)):
            printline=""
            for xi in range(0,len(map[yi])):
                c= map[yi][xi]
                if x==xi and y==yi:
                    c=icon[facing]
                printline += c
            print( printline )
    print(f'{x},{y}')
    pprint(task)
    if task[0] == "move":
        for s in range(0,task[1]):
            step = get_step(map,x,y,facing)
            pprint(step)
            if map[step[1]][step[0]] == "#":
                print( "BONK!" )
                break
            x = step[0]
            y = step[1]
    if task[0] == "turn":
        facing = (facing + task[1])%4

answer = (y+1)*1000 + (x+1)*4 + facing



print( f'PART 1 = {answer}' )

