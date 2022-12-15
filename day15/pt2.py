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



bdict = {}

    # g4 - +1186 pretax
    # g5 - +1548 pretax
data = []
first = True

for line in lines:
    if line=="":
        continue
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
    if first:
        first=False
        miny=sy
        maxy=sy
        maxrange=brange
    else:
        if sy<miny:
            miny=sy
        if sy>maxy:
            maxy=sy
        if brange>maxrange:
            maxrange=brange


for sen in data:
    bdict[f'{sen[0][0]},{sen[0][1]}']=sen[0]
    bdict[f'{sen[1][0]},{sen[1][1]}']=sen[1]
beacons = bdict.values()


miny = 0
maxy = 4000000
for y in range( miny,maxy+1 ):
    #print()
    if y%40000 == 0:
        print( y/40000 )

    skip = False
    ex_ranges = []
    for sen in data:
        # calculate per beacon exclusion
        #pprint(sen)
        # calculate exclusion range in row y
        yoffset = abs( sen[0][1]-y )
        if yoffset > sen[2] :
            continue
        size = sen[2]-yoffset
        ex_x1 = sen[0][0]-size
        ex_x2 = sen[0][0]+size
        if ex_x1 <=0 and ex_x2 >= 4000000:
            skip = True
            break
        ex_range = [ex_x1,ex_x2]
        ex_ranges.append( ex_range )
 
    # sort by starting pos
    ex_ranges.sort( key= lambda foo: foo[0] )
    print( f'y={y}') 
    pprint( ex_ranges )
    if skip:
        print( "SKIP!!")
        continue
    for beacon in beacons:
        if beacon[1]==y:
            ex_ranges.append( [beacon[0],beacon[0]] )
    
    merged = True
    while merged:
        merged = False
        for i in range(0,len(ex_ranges)):
            for j in range(0,len(ex_ranges)):
                if i==j:
                    continue
                # see if these ranges overlap OR abut is either the start or end of one inside the other
                if ex_ranges[i][0] >= ex_ranges[j][0] and ex_ranges[i][0] <= ex_ranges[j][1]+1:
                    # range i starts within range j
                    # so from the start of j to the end of the max of i and j
                    new_range = [ ex_ranges[j][0], max( ex_ranges[i][1], ex_ranges[j][1] ) ]
                elif ex_ranges[j][0] >= ex_ranges[i][0] and ex_ranges[j][0] <= ex_ranges[i][1]+1:
                    # range j starts within range i
                    # so from the start of j to the end of the max of i and j
                    new_range = [ ex_ranges[i][0], max( ex_ranges[i][1], ex_ranges[j][1] ) ]
                else:
                    continue
                new_ex_ranges = [ new_range ]
                for k in range( 0,len(ex_ranges) ):
                    if k==i or k==j:
                        # lost the merged ranges
                        continue
                    new_ex_ranges.append(ex_ranges[k])
                ex_ranges = new_ex_ranges
                merged = True
                break
            if merged:
                break
    if len(ex_ranges)>1:
        print(y)
        pprint(ex_ranges)    
        # find the smaller range end and add 1
        pt2x = min(ex_ranges[0][1], ex_ranges[1][1])+1
        print(pt2x)
        break
    

pt2 = y+4000000*pt2x
print( f'PART 2 = {pt2}' )

 # 6220655 too high
