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

data = []

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

for sen in data:
    bdict[f'{sen[0][0]},{sen[0][1]}']=sen[0]
    bdict[f'{sen[1][0]},{sen[1][1]}']=sen[1]
beacons = bdict.values()

K = 4000000
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    K = 20
miny = 0
maxy = K
for y in range( miny,maxy+1 ):
    #print()
    if y%40000 == 0:
        print( y/40000 )
    ex_ranges = []
    for sen in data:
        # calculate per beacon exclusion
        #pprint(sen)
        # calculate exclusion range in row y
        yoffset = abs( sen[0][1]-y )
        if yoffset > sen[2] :
            continue
        size = sen[2]-yoffset
        ex_ranges.append( [ sen[0][0]-size, sen[0][0]+size ] )
 
    # sort by starting pos
    ex_ranges.sort( key= lambda foo: foo[0] )
    #print( f'y={y}') 
    #pprint( ex_ranges )

    # start!?
    if ex_ranges[0][0] > 0:
        print( "EH?" )
        pprint( ex_ranges)
        exit()
    filled_up_to = 0
    # look for a gap between ranges, ie the next range starts 2 after the last ended
    for i in range(0,len(ex_ranges)-1):
        x1 = ex_ranges[i][1] # end of current range
        if x1>filled_up_to:
            filled_up_to = x1
        x2 = ex_ranges[i+1][0] # start of next range
        if x2==filled_up_to+2:
            print("YAY")
            print(filled_up_to+1)
            print(y)
            pt2 = y+4000000*(filled_up_to+1)
            print( f'PART 2 = {pt2}' )

            exit()

#    for beacon in beacons:
#        if beacon[1]==y:
#            ex_ranges.append( [beacon[0],beacon[0]] )
    
    


 # 6220655 too high
