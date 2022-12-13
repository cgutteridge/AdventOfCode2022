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

grid = []
map  = []
todo = []
y=0
for line in lines:
    if line == "":
        continue
    row = []
    mrow= []
    x=0
    for c in list(line):
        if c=='S':
            start=[x,y]
            c = 'a'
        if c=='E':
            end=[x,y]
            c = 'z'
        row.append( ord(c)-ord("a") )
        mrow.append(-1)
        todo.append( [x,y] )
        x+=1
    grid.append(row)
    map.append(mrow)
    y+=1

map[start[1]][start[0]] = 0

moves = [ [0,-1],[0,1],[-1,0],[1,0]]

while len(todo)>0:
    #pprint(map)
    #pprint(grid)
    print( len(todo) )
    newtodo = {}
    set_something = False
    for cursor in todo:
        x = cursor[0]
        y = cursor[1]
        #print()
        #print(f'CONSIDER = {x},{y}')
        targets = []
        for move in moves:
            nx=x+move[0]
            ny=y+move[1]
            #print(f'{x},{y}->{nx},{ny}')
            if nx>=0 and nx<len(grid[0]) and ny>=0 and ny<len(grid):
                offset = grid[ny][nx]-grid[y][x]
                #print(f'{x},{y}->{nx},{ny} -- {offset}')
                if map[y][x]==-1:
                    #can't do this now, but let's keep it on the list
                    newtodo[f'{x},{y}'] = [x,y]
                elif offset<=1:
                    score = map[y][x]+1
                    if map[ny][nx] == -1 or map[ny][nx] > score:
                        map[ny][nx] = score
                            #print( f'set {nx},{ny}={score}' )
                        newtodo[f'{nx},{ny}'] = [nx,ny]
                        set_something = True
        #pprint(map)
    if not set_something:
        break
    todo = newtodo.values()

    
pt1=map[end[1]][end[0]]
pprint(map)

print(f'PT1: {pt1}')

