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

size = 50
#   01
#   2
#  34
#  5
sides = [[1,0],[2,0],[1,1],[0,2],[1,2],[0,3]]
exits = [
        { "<":[3,">","!"], "^":[5,">","="] },               # 0
        { "^":[5,"^","="], ">":[4,"<","!"], "v":[2,"<","="] },  # 1
        { "<":[3,"v","="], ">":[1,"^","="] },               # 2
        { "<":[0,">","!"], "^":[2,">","="] },               # 3
        { ">":[1,"<","!"], "v":[5,"<","="] },               # 4
        { "<":[0,"v","="], "v":[1,"v","="], ">":[4,"^","="] }   # 5
        ]
pmap=False

if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    pmap=True
    size = 4
    #    0
    #  123
    #    45
    sides = [[2,0],[0,1],[1,1],[2,1],[2,2],[3,2]]
    exits = [
            { "<":[2,"v","="], "^":[1,"v","!"], ">":[5,"<","!"] },  # 0
            { "^":[0,"v","!"], "<":[5,"^","!"], "v":[4,"^","!"] },  # 1
            { "^":[0,">","="], "v":[4,">","!"] },               # 2
            { ">":[5,"v","!"] },                            # 3
            { "<":[2,"^","!"], "v":[1,"^","!"] },               # 4
            { "^":[3,"<","!"], ">":[0,"<","!"], "v":[1,">","!"] }   # 5
            ]

ricon = { ">":"<", "<":">", "v":"^", "^":"v" }
# check invese paths
for ei in range(0,len(exits)):
    for d in exits[ei]:
        path = exits[ei][d]
        # get the path that is the opposite direction to the way we come in
        path2 = exits[path[0]][ricon[path[1]]]
        if path2[0] != ei:
            print("EEK path2[0] and ei don't match")
            exit()
        if path2[1] != ricon[d]:
            print("EEK path2[1] is not reverse of d")
            exit()
        if path2[2] != path[2]:
            print("EEK flip mismatch")
            exit()


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
icon_to_n = {">":0,"v":1,"<":2,"^":3}

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
        return [xi,yi,facing]

    print(f'WRAP! {x},{y} {icon[facing]} ')

    # work out what face we are in
    fx=int(x/size)
    fy=int(y/size)
    for si in range(0,len(sides)):
        if fx==sides[si][0] and fy==sides[si][1]:
            side=si
    wrap = exits[side][icon[facing]]
    if facing==0 or facing==2:
        pos = y-fy*size
    if facing==1 or facing==3:
        pos = x-fx*size

    print(f'Leaving {side} facing {icon[facing]} sidepos={pos}')

    # set new facing
    facing = icon_to_n[wrap[1]]

    # if flip
    if wrap[2]=="!":
        pos = (size-1) - pos
        print( "FLIP!")

    # set base position of new face
    newside = wrap[0]
    fx = sides[newside][0]
    fy = sides[newside][1]

    # set x,y
    if facing==0:
        xi = fx*size
        yi = fy*size + pos
    elif facing==1:
        xi = fx*size + pos
        yi = fy*size
    elif facing==2:
        xi = fx*size + (size-1)
        yi = fy*size + pos
    elif facing==3:
        xi = fx*size + pos
        yi = fy*size + (size-1)
    else:
        print("BAD FACING")
        print(facing)
        exit()

    print(f'Entering {newside} sideco={fx},{fy} facing {icon[facing]} sidepos={pos} x={xi} y={yi}')
    return [xi,yi,facing] 

been = {}
for task in plan:
    if pmap:
        print()
        for yi in range(0,len(map)):
            printline=""
            for xi in range(0,len(map[yi])):
                c= map[yi][xi]
                code = f'{xi},{yi}'
                if code in been:
                    c=been[code]
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
            facing = step[2]
            been[f'{x},{y}']=icon[facing]
    if task[0] == "turn":
        facing = (facing + task[1])%4
        been[f'{x},{y}']=icon[facing]

answer = (y+1)*1000 + (x+1)*4 + facing



print( f'PART 1 = {answer}' )

