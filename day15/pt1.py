#!/usr/bin/python3

import sys
import re
from pprint import pprint,pformat

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")

    # g4 - +1186 pretax
    # g5 - +1548 pretax
data = []
first = True

for line in lines:
    if line=="":
        continue
    print( line)
    line=re.sub("[,:]", "", line)
    #Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    words = line.split( " " )
    sxb = words[2].split("=")
    syb = words[3].split("=")
    bxb = words[8].split("=")
    byb = words[9].split("=")
    sx = int(sxb[1])
    sy = int(syb[1])
    bx = int(bxb[1])
    by = int(byb[1])
    brange = abs(bx-sx)+abs(by-sy)
    r = [[sx,sy],[bx,by],brange]
    data.append(r)
    pprint(r)
    if first:
        first=False
        minx=sx
        maxx=sx
        maxrange=brange
    else:
        if sx<minx:
            minx=sx
        if sx>maxx:
            maxx=sx
        if brange>maxrange:
            maxrange=brange

y=10 
pt1=0
r="          "
l="          "
for x in range(minx-maxrange,maxx+maxrange):
    # is spot >= away from the cutoff of each beacon
    count = False
    for sensor in data:
        bdist = abs(x-sensor[0][0])+abs(y-sensor[0][1])
        if sensor[1][0]==x and sensor[1][1]==y:
            #it can't be on a beacon
            count = False
            break
        if bdist<=sensor[2]:
            # we are nearer to this sensor than it's beacon
            count = True
            break
    if x%5==0:
        mark = str(x)
        l = l[0:-len(mark)]+mark+"|"
    else:
        l += " "
    if count:
        pt1+=1
        r+="#"
    else:
        r+="."
    print(x)
print(l)
print(r)

print( f'PART 1 = {pt1}' )

 # 6220655 too high
