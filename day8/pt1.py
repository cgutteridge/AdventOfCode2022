#!/usr/bin/python3

import sys
from pprint import pprint

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'

with open(file, 'r') as f:
	lines = f.read().split("\n")


tree = []
# test mode has multiple lines
for line in lines:
    if line=="":
        continue
    # find marker
    # loop over 4 char sets, finding first that's all unique
    chars = list(line)
    row = []
    for char in chars:
        row.append( int(char) )
    tree.append(row)

xw = len(tree[0])
yw = len(tree)
print(xw,yw)

########################################
def visible(x,y):
    #print(f'{x},{y}: ')
    if x==0:
        return True
    if x==xw-1:
        return True
    if y==0:
        return True
    if y==yw-1:
        return True

    hid = False
    for xi in range(0,x):
        #print(f' L: {xi},{y} ')
        if(tree[y][xi]>=tree[y][x]):
            hid=True
    if not hid:
        #print(f'{x},{y}: left')
        return True

    hid = False
    for xi in range(x+1,xw):
        #print(f' R: {xi},{y} ')
        if(tree[y][xi]>=tree[y][x]):
            hid=True
    if not hid:
        #print(f'{x},{y}: right')
        return True

    hid = False
    for yi in range(0,y):
        #print(f' T: {x},{yi} ')
        if(tree[yi][x]>=tree[y][x]):
            hid=True
    if not hid:
        #print(f'{x},{y}: top')
        return True

    hid = False
    for yi in range(y+1,yw):
        #print(f' B: {x},{yi} ')
        if(tree[yi][x]>=tree[y][x]):
            hid=True
    if not hid:
        #print(f'{x},{y}: bottom')
        return True

    return False



########################################
pt1=0

for y in range(0,yw):
    r=""
    for x in range(0,xw):
        #print(f'{x},{y}...')
        v = visible(x,y)
        #print(f'{x},{y} - {v}')
        if v:
            r += "-"
        else:
            r += "X"
        if v:
            pt1 += 1
    print(r)


print(f'PT1: {pt1}')

# 1242 too low
