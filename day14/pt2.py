#!/usr/bin/python3

import sys
from pprint import pprint,pformat

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")

grid = []
for y in range(0,500):
    row = []
    for x in range(0,1000):
        row.append(' ')
    grid.append(row)

maxy=0
for line in lines:
    if line == "":
        continue
    #525,161 -> 525,156 -> 525,161 
    nodes_text = line.split( " -> " )
    nodes = []
    for node_text in nodes_text:
        n_text = node_text.split(",")
        #pprint( n_text )
        nodes.append([int(n_text[0]),int(n_text[1])])
    #pprint(nodes)
    for p in range(1,len(nodes)):
        n1 = nodes[p-1]
        n2 = nodes[p]
        if n1[1]>maxy:
            maxy=n1[1]
        if n2[1]>maxy:
            maxy=n2[1]
        xs = n2[0]-n1[0]
        ys = n2[1]-n1[1]
        if xs!=0:
            xstep = int(xs/abs(xs))
        else:
            xstep = 0
        if ys!=0:
            ystep = int(ys/abs(ys))
        else:
            ystep = 0
        #pprint(['line',n1,n2,xstep,ystep])
        x = n1[0]
        y = n1[1]
        while x!=n2[0] or y!=n2[1]:
            grid[y][x]='#'
            #pprint([x,y])
            x += xstep
            y += ystep
        grid[y][x]='#'
for x in range(0,1000):
    grid[maxy+2][x]='#'
pt2=0
while True:
#    for yp in range(0,12):
#        print( "".join(grid[yp][484:513])+"|")
    x=500
    y=0
    # if start is blocked, stop
    if grid[y][x]=='o':
        break
    # if sand can't move, do next loop

    while True:
        #pprint([x,y])
        if y==499:
            break
        if grid[y+1][x]==" ":
            y += 1
        elif grid[y+1][x-1] == " ":
            y += 1
            x -= 1
        elif grid[y+1][x+1] == " ":
            y += 1
            x += 1
        else:
            pt2+=1
            grid[y][x]="o"
            break
    if y==499:
        break




print( f'PART 2 = {pt2}' )


