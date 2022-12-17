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
gusts = list( lines[0] )
#pprint(gusts)

rocks = [
        [[0,0],[1,0],[2,0],[3,0]], # - 
        [[1,0],[0,1],[1,1],[2,1],[1,2]], # +
        [[0,0],[1,0],[2,0],[2,1],[2,2]], # rev L
        [[0,0],[0,1],[0,2],[0,3]], # |
        [[0,0],[0,1],[1,0],[1,1]] # square
        ]
widths  = [4,3,3,1,2]
heights = [1,3,3,4,2]
syms = ["-","+","L","|","#"]

grid=[]
for i in range(0,5000):
    grid.append(['.','.','.','.','.','.','.'])

top_row=0
def debug(grid):
    print()
    h = 12
    top = max(11,top_row)
    for i in range(0,h):
        row_y = top-i
        print("|"+"".join(grid[row_y])+"| "+str(row_y))
    
    #print( "+-------+")

print(f'gusts = {len(gusts)}')
gust = 0
# x,y is bottom left of rock
for i in range(0,2022):

    debug(grid)
    print(f'top row = {top_row}, rock = {i}')
    rock = rocks[i%5]
    width = widths[i%5]
    height = heights[i%5]
    sym = syms[i%5]
    y = top_row+3 
    x = 2

    moving = True
    while moving:
        print(f'GUST n = {gust}')
        d = 1
        if gusts[gust%len(gusts)]=="<":
            d=-1
        gust+=1
        pprint([[x,y],d])
    
        # SIDEWAYS
    
        # check gust does not hit a wall
        move_sideways = True
        if x+d<0 or x+d+width>7:
            move_sideways=False
        else:
            # check none of the elements would hit a resting rock
            for offset in rock:
                if grid[y+offset[1]][x+offset[0]+d] != ".":
                    move_sideways=False
                    break
        if move_sideways:
            x+=d
            print(d)
        else:
            print("NO SIDEWAYS")
    
        # DOWN

        # stop if any rock bit has floor or rock directly below
        if y==0:
            moving = False
        else:
            for offset in rock:
                if grid[y+offset[1]-1][x+offset[0]] != ".":
                    moving = False
                    break
        if not moving:
            for offset in rock:
                grid[y+offset[1]][x+offset[0]] = sym
            if y+height>top_row:
                top_row=y+height
        else:
            y -= 1
        
                    


    
    


pt1 = top_row

print( f'PART 1 = {pt1}' )

