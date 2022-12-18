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

grid = {}
first = True
for line in lines:
    if line == "":
        continue
    xyz_s = line.split( "," )
    x = int(xyz_s[0])
    y = int(xyz_s[1])
    z = int(xyz_s[2])
    grid[line]="#"
    if first:
        xmin=x
        ymin=y
        zmin=z
        xmax=x
        ymax=y
        zmax=z
        first = False
    else:
        if x>xmax:
            xmax=x
        if y>ymax:
            ymax=y
        if z>zmax:
            zmax=z
        if x<xmin:
            xmin=x
        if y<ymin:
            ymin=y
        if z<zmin:
            zmin=z

pprint([
    [xmin,ymin,zmin],
    [xmax,ymax,zmax]
    ])


def print_grid(grid):
    print()
    print("GRID START")
    print()
    for z in range(zmin,zmax+1):
        for y in range(ymin,ymax+1):
            r = ""
            for x in range(xmin,xmax+1):
                code = f'{x},{y},{z}'
                if not code in grid:
                    r += " "
                else:
                    r += grid[code]
            print(r)
        print()
    print("GRID END")


#print_grid(grid)



# mark all exterior spaces as flooded and pending to flood more
# mark other spaces as air, for now
to_flood = []
for x in range(xmin,xmax+1):
    for y in range(ymin,ymax+1):
        for z in range(zmin,zmax+1):
            code = f'{x},{y},{z}'
            if x==xmin or x==xmax or y==ymin or y==ymax or z==zmin or z==zmax:
                #print( "EDGE!")
                if not code in grid:
                    grid[code] = "x" # STEAM
                    to_flood.append([x,y,z])
            else:
                #print("NOT EDGE")
                # inner location
                if not code in grid:
                    #print( "AIR" )
                    grid[code] = "." # AIR

#print_grid(grid)

dirs = [
        [0,0,1],
        [0,0,-1],
        [0,1,0],
        [0,-1,0],
        [1,0,0],
        [-1,0,0]]

while len(to_flood)>0:
    c = to_flood.pop()
    for dir in dirs:
        x1 = c[0]+dir[0]
        y1 = c[1]+dir[1]
        z1 = c[2]+dir[2]
        # only worry about air inside the grid we defined
        code = f'{x1},{y1},{z1}'
        if code in grid and grid[code]==".":
            #print("FLOOD")
            grid[code] = "x"
            to_flood.append( [x1,y1,z1] )

print( "FINAL")
print_grid(grid)

result = 0
for x in range(xmin,xmax+1):
    for y in range(ymin,ymax+1):
        for z in range(zmin,zmax+1):
            # if this in internal, count each external edge
            code = f'{x},{y},{z}'
            print( "NOT-EDGE : "+code)
            if grid[code] == "#":
                for dir in dirs:
                    x1 = x+dir[0]
                    y1 = y+dir[1]
                    z1 = z+dir[2]
                    if x1<xmin or x1>xmax or y1<ymin or y1>ymax or z1<zmin or z1>zmax:
                        # grid edges are always external
                        result += 1
                        continue
                    code1 = f'{x1},{y1},{z1}'
                    print( "* CODE "+code1)
                    if grid[code1] == "x":
                        result += 1




print( f'PART 2 = {result}' )

