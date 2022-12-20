#!/usr/bin/python3

import time
import sys
import re
import copy
from pprint import pprint,pformat

t0 = seconds = time.time()
tn = t0

def timecheck():
    global tn
    global t0
    new_time = time.time()
    r = int(new_time-tn)
    a = int(new_time-t0)
    tn=new_time
    return f'section_t={r} since_start={a}'

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
    y = 10
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")

def showring(ring,start):
    v = [str(ring[start][0])]
    i = ring[start][2]
    while i!=start:
        v.append(str(ring[i][0]))
        i = ring[i][2]
    print( " ".join( v ))



# store [ value, previndex, nextindex ]
ring = []
i=0
for line in lines:
    if line=="":
        continue
    v = int(line)
    if v==0:
        zero_index = i
    ring.append([v*811589153,i-1,i+1])
    i+=1
size=len(ring)
ring[0][1] = size-1
ring[size-1][2] = 0

showring(ring,zero_index)
pprint(ring)
# mix it up
for loop in range(0,10):
    print(f'LOOP {loop+1}')
    for mix_index in range(0,size):
    # pprint(ring)
        #showring(ring,zero_index)
        item = ring[mix_index]
        #print( f'MOVING {item[0]}')
        if item[0]==0:
            continue
    
        # remove item from the ring
        # heal the gap
        ring[ item[1] ][2] = item[2] # prev's next becomes item's next
        ring[ item[2] ][1] = item[1] # next's prev becomes item's prev
    
        # 2 forward   1 backwards
        dir = 2
        moves = item[0] % (size-1)
        if item[0]<0:
            dir = 1
            moves = (-item[0]) % (size-1)
            moves+= 1 # move one extra backwards so we always insert AFTER the final spot

        i = mix_index
        while moves > 0:
            i = ring[i][dir]
            moves-=1
    
        # put the item back into the ring AFTER the item with index i
        prv = i
        nex = ring[i][2]
        ring[mix_index][1]=prv
        ring[mix_index][2]=nex
        ring[prv][2] = mix_index
        ring[nex][1] = mix_index
    showring(ring,zero_index)
            
    

answer = 0

i = zero_index
for j in range(0,3):
    for k in range(0,1000):
        i = ring[i][2]
    print( ring[i][0] )
    answer += ring[i][0]


print( size )
print( f'PART 2 = {answer}' )
# not  -8623134750625


