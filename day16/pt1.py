#!/usr/bin/python3

import sys
import re
import copy
from pprint import pprint,pformat

file = 'data'
y = 2000000
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
    y = 10
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")

rooms = {}
#Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

important = ["AA"]
to_open = {}
for line in lines:
    if line=="":
        continue
    line=re.sub(",", "", line)
    line=re.sub(";", "", line)
    line=re.sub("=", " ", line)
    words = line.split( " " )
    vid = words[1]
    rate = int(words[5])
    to = words[10:]
    room = {"vid":vid,"rate":rate,"to":to,"routes":{}}
    rooms[vid]=room
    if rate>0:
        important.append(vid)
        to_open[vid]=True

# find distance between important rooms 
for vid in important:
    dists = {vid:0}
    edge_rooms = [vid]
    dist = 0
    while len(edge_rooms):
        new_edge_rooms = []
        dist += 1
        for vid2 in edge_rooms:
            for vid3 in rooms[vid2]["to"]:
                if not vid3 in dists:
                    dists[vid3] = dist
                    new_edge_rooms.append(vid3)
        edge_rooms = new_edge_rooms
    # only log important routes
    # never go back to AA as it wasn't really important
    # don't include the current room
    for vid4 in important:
        if vid4 != "AA" and vid4 != vid:
            rooms[vid]["routes"][vid4]=dists[vid4]

# pos is where we are now. 
# not_open is an array of as yet unopened valves
# time is the time remaining
# assume every action is move to an unopened valve and open it
def best_score( pos, not_open, time, indent = "" ):
    print( indent+"Consider "+pos )
    best = 0
    # look through our possible routes
    for to_open in not_open:
        #print( indent+"* go and open "+to_open )
        open_time = time+rooms[pos]["routes"][to_open]+1
        if open_time>=30:
            #print( indent+"  NO TIME")
            continue
        # this valve opened at the end of open_time so scores 30-open_time x it's rate
        score_from_valve = (30-open_time) * rooms[to_open]["rate"]
        #print( indent+f"  (30-{open_time})*{rooms[to_open]['rate']} = {score_from_valve}")
        new_not_open = dict(not_open)
        del new_not_open[to_open]
        score_from_routes = best_score( to_open, new_not_open, open_time, indent+"    ")
        score=score_from_routes+score_from_valve
        #print( indent+f" score={score_from_valve}+{score_from_routes} = {score}")
        if score>best:
            best = score
    #print( indent+"Result for "+pos+" "+str(best) )
    return best


pprint(rooms )
pt1 = best_score( "AA", to_open, 0 )

print( f'PART 1 = {pt1}' )

