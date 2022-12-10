#!/usr/bin/python3

import sys
from pprint import pprint

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'

with open(file, 'r') as f:
	lines = f.read().split("\n")

w = 5
h = 5
head = [0,4]
tail = [0,4]

def report():
    for y in range(0,h):
        row = []
        for x in range(0,w):
            if x==head[0] and y==head[1]:
                row.append("H")
            elif x==tail[0] and y==tail[1]:
                row.append("T")
            else:
                row.append(".")
        print( "".join(row) )

dirs = {
        "U": [0,-1],
        "D": [0,1],
        "L": [-1,0],
        "R": [1,0]
        }
been = {}
for line in lines:
    if line == "":
        continue
    args = line.split( " " )
    vec = dirs[args[0]]
    dist = int(args[1])
    for i in range(0,dist):
        head[0] += vec[0]
        head[1] += vec[1]   
        print ("head now")
        pprint( head )
        print ("tail now")
        pprint( tail )
        if vec[0]!=0 and tail[0] == head[0] - 2 * vec[0]:
            tail[0] = head[0] - vec[0]
            tail[1] = head[1]
            print("TR1")
        if vec[1]!=0 and tail[1] == head[1] - 2 * vec[1]:
            tail[0] = head[0]
            tail[1] = head[1] - vec[1]
            print("TR2")
        been[f'{tail[0]},{tail[1]}'] = True
        pprint( line )
        pprint( head )
        pprint( tail )
        report()
        print()

pprint(been)


pt1=len(been)

print(f'PT1: {pt1}')

