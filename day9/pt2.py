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

w = 25
h = 25
snake = [[10,15],[10,15],[10,15],[10,15],[10,15],[10,15],[10,15],[10,15],[10,15],[10,15]]

def report():
    for y in range(0,h):
        row = []
        for x in range(0,w):
            for i in range(0,len(snake)):
                if x==snake[i][0] and y==snake[i][1]:
                    if i==0:
                        row.append("H")
                    else:
                        row.append(str(i))
                    break
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
        snake[0][0] += vec[0]
        snake[0][1] += vec[1]   
        for tail_i in range( 1,len(snake)):
            offset = [ snake[tail_i][0]-snake[tail_i-1][0], snake[tail_i][1]-snake[tail_i-1][1] ]
            if offset[0] == 2 or offset[0] == -2:
                x_dir = offset[0]/abs(offset[0])
                # catch up in the x dir
                snake[tail_i][0] -= x_dir
                # move one space in the y dir too if needed
                if( offset[1] != 0 ):
                    y_dir = offset[1]/abs(offset[1])
                    snake[tail_i][1] -= y_dir
            elif offset[1] == 2 or offset[1] == -2:
                y_dir = offset[1]/abs(offset[1])
                # catch up in the y dir
                snake[tail_i][1] -= y_dir
                # move one space in the y dir too if needed
                if( offset[0] != 0 ):
                    x_dir = offset[0]/abs(offset[0])
                    snake[tail_i][0] -= x_dir
            been[f'{snake[9][0]},{snake[9][1]}'] = True
    report()
    print()

pprint(been)


pt1=len(been)

print(f'PT1: {pt1}')

