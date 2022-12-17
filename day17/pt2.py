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
pprint(len(gusts))

rocks = [
        [[0,0],[1,0],[2,0],[3,0]], # - 
        [[1,0],[0,1],[1,1],[2,1],[1,2]], # +
        [[0,0],[1,0],[2,0],[2,1],[2,2]], # rev L
        [[0,0],[0,1],[0,2],[0,3]], # |
        [[0,0],[0,1],[1,0],[1,1]] # square
        ]
rockwidths  = [4,3,3,1,2]
rockheights = [1,3,3,4,2]
syms = ["-","+","L","|","#"]

grid=[]
for i in range(0,3000):
    grid.append(['.','.','.','.','.','.','.'])

g_off = 0
top_row=0
def debug(grid):
    print()
    h = 12
    top = max(11,top_row)
    for gy in range(0,h):
        row_y = top-gy
        print("|"+"".join(grid[row_y-g_off])+"| "+str(row_y))
    


tops = [0,0,0,0,0,0,0]
print(f'gusts = {len(gusts)}')
gust = 0
# x,y is bottom left of rock
seen = {}
heights={}
for i in range(0,2022):
    print("-")
    # normalise tops
    mintop=tops[0]
    for top in tops:
        if top<mintop:
            mintop=top
    while mintop>g_off+10:
        print("TRIM")
        del grid[0]
        grid.append(['.','.','.','.','.','.','.'])
        g_off+=1


    print(f'goff={g_off}')
    tstr=""
    for j in range(0,len(tops)):
        tstr+=","+str(tops[j]-mintop)

    #code = f'{i%5},{gust%len(gusts)}{tstr}'
    code = f'{i%5},{gust%len(gusts)}|'
    for row in grid:
        s = "".join( row )
        if s!= ".......":
            code+=s+"|"

    debug(grid)
    print( i )
    print( code )
    if code in seen:
        print("LOOP")
        pprint(seen[code])
        print(i)
        loop_start = seen[code]
        loop_start_size = heights[seen[code]]
        loop_size_inc = top_row-heights[seen[code]]
        loop_len = i-seen[code]
        pprint([loop_start,loop_len,loop_start_size,loop_size_inc])
        target = 1000000000000

        height = loop_start_size
        target-= loop_start
        pprint([height,target])

        loops = int(target / loop_len )
        height+= loops * loop_size_inc
        target = target % loop_len
        pprint([height,target,loops])

        print(height)
        height += heights[loop_start+target]-loop_start_size
        print( "FINAL")
        print(height)

        break
    seen[code]=i
    heights[i]=top_row

    if i % 100000 == 0:
        print()
        print(i)
        print(code)
        print(len(seen))
   # if gust % 10000 < 4:
   #     print(f'i {i} / {len(gusts)}')
#    if gust % len(gusts)<4:
#        print(f'gustloop {int(gust/len(gusts))}')



    #print(code)
    #debug(grid)
    #print(tstr)
    #print(f'top row = {top_row}, rock = {i}')
    rock = rocks[i%5]
    width = rockwidths[i%5]
    height = rockheights[i%5]
    sym = syms[i%5]
    y = top_row+3 
    x = 2
    print(f'rock start y = {y}')
    moving = True
    while moving:
        #print(f'GUST n = {gust}')
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
                if grid[y+offset[1]-g_off][x+offset[0]+d] != ".":
                    move_sideways=False
                    break
        if move_sideways:
            x+=d
            #print(d)
        #else:
            #print("NO SIDEWAYS")
    
        # DOWN

        # stop if any rock bit has floor or rock directly below
        if y==0:
            moving = False
            #print( "HIT FLOOR")
        else:
            print( f'y={y}')
            pprint( rock )
            for offset in rock:
                #print( f'consider : {x}+{offset[0]},{y}+{offset[1]}')
                if grid[y+offset[1]-1-g_off][x+offset[0]] != ".":
                    moving = False
                    #print( f"HIT BLOCK {x+offset[0]},{y+offset[1]-1-g_off} .. {y}+{offset[1]}-1-{g_off} .. {grid[y+offset[1]-1-g_off][x+offset[0]]}")
                    break
        if not moving:
            for offset in rock:
                grid[y+offset[1]-g_off][x+offset[0]] = sym
                if y+offset[1]+1 > tops[x+offset[0]]:
                    tops[x+offset[0]] = y+offset[1]+1 
            print(f'tr={top_row},y={y},h={height}')
            if y+height>top_row:
                top_row=y+height
        else:
            y -= 1
        
                    


    
    


pt1 = top_row

print( f'PART 1 = {pt1}' )

