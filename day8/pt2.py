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
def score(x,y):
    print(f'{x},{y}: ')

    if x==0:
        return 0
    if x==xw-1:
        return 0
    if y==0:
        return 0
    if y==yw-1:
        return 0

    ranges = []

    r = []
    for xi in range(x-1,-1,-1):
        r.append([xi,y])
    ranges.append(r)

    r = []
    for xi in range(x+1,xw):
        r.append([xi,y])
    ranges.append(r)

    r = []
    for yi in range(y-1,-1,-1):
        r.append([x,yi])
    ranges.append(r)

    r = []
    for yi in range(y+1,yw):
        r.append([x,yi])
    ranges.append(r)

    # ranges go from treehouse out
    # find the position of the biggest tree equal or bigger to our treehouse or score whole row
    score = 1
    for r in ranges:
        pprint(r)
        s=len(r)
        i=0
        for t in r:
            i += 1
            this_tree = tree[t[1]][t[0]]
            if( this_tree >= tree[y][x] ):
                s = i
                break
        print(s)
        score*=s
    return score

########################################
pt2=0

for y in range(0,yw):
    r=""
    for x in range(0,xw):
        #print(f'{x},{y}...')
        print("----")
        s = score(x,y)
        print(f'*** {x},{y} - {s}')
        if s>pt2:
            pt2=s


print(f'PT2: {pt2}')

