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


#Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
bps = []
for line in lines:
    if line == "":
        continue
    bp = { "rec":{} }
    a = line.split(":")
    b = a[0].split(" ")
    bp["number"] = int(b[1])
    c = a[1].split(".")
    for d in c:
        if d=="":
            continue
        e = d.split( " costs " )
        f = e[0].split( " " )
        g = e[1].split( " and " )
        res = f[2]
        costs = {}
        for h in g:
            i = h.split(" ")
            costs[i[1]]=int(i[0])
        bp["rec"][res]=costs
    bps.append(bp)

for bp in bps:
    bp["max_ore"] = 0
    # last day to build geode = 23
    # last day to build obsidian = geode-bp[rec][geode][obsidian]-1
    # last day to build clay = obsidian-bp[rec][obsidian][clay]-1A
    bp["last_obsidian"] = 23 - bp["rec"]["geode"]["obsidian"]+1
    bp["last_clay"] = bp["last_obsidian"] - bp["rec"]["obsidian"]["clay"]+1

    for rec in bp["rec"][res]:
        if bp["rec"][res]["ore"]>bp["max_ore"]:
            bp["max_ore"]=bp["rec"][res]["ore"]
pprint(bps)

# {'number': '2',
#  'rec': {'clay': {'ore': 3},
#          'geode': {'obsidian': 12, 'ore': 3},
#          'obsidian': {'clay': 8, 'ore': 3},
#          'ore': {'ore': 2}}}]

types= ["ore","clay","obsidian","geode" ]

def can_build( state, bp, todo ):
    #pprint(["CB",state,bp,todo])
    if todo==4:
        return [{"bots":{},"stock":state["stock"],"built":{"ore":False,"clay":False,"obsidian":False,"geode":False}}]
    res = types[todo]
    # work out how many of typ res we could buy given the stock
    max_bot = 99999999
    for cost_res in bp["rec"][res]:
        v = int( state["stock"][cost_res]/bp["rec"][res][cost_res] )
        if v < max_bot:
            max_bot = v
    #print(f'can afford {max_bot} of {res}')
    opts = []
    for res_buy in range(0,max_bot+1):
        # every amount including zero and max
        new_stock = dict(state["stock"])
        for cost_res in bp["rec"][res]:
            new_stock[cost_res] -= res_buy * bp["rec"][res][cost_res]
            if( new_stock[cost_res] < 0 ):
                print( "EEK")
                pprint(state)
                pprint(bp["rec"][res])
                print(f' buying {res_buy} of {cost_res} at {bp["rec"][res][cost_res]}' )
                print( new_stock )
                exit()
        cbopts = can_build( {"bots":state["bots"],"stock":new_stock},bp,todo+1)
        for cbopt in cbopts:
            cbopt["bots"][res]=res_buy+state["bots"][res]
            if res_buy > 0:
                cbopt["built"][res]=True
            opts.append( cbopt )
    return opts

cache = {}
hits = 0
its = 0

def best_outcome( time, state, bp, indent="" ):
    if time==24:
        return state["stock"]["geode"]

    # if ore income is more than max ore skip?
    if state["bots"]["ore"]>2:
        return 0
#    if state["bots"]["clay"]>5:
#        return 0

    if state["bots"]["obsidian"]==0 and time>bp["last_obsidian"]:
        #print( "OBS")
        return 0
    if state["bots"]["clay"]==0 and time>bp["last_clay"]:
        #print( "CLAY")
        return 0
    global its
    global hits
    global cache
    code=f'{time},{state["bots"]["ore"]},{state["bots"]["clay"]},{state["bots"]["obsidian"]},{state["bots"]["geode"]},{state["stock"]["ore"]},{state["stock"]["clay"]},{state["stock"]["obsidian"]},{state["stock"]["geode"]}'
    #print(indent+f' time={time} {code}')
    if code in cache:
        return cache[code]
    #pprint(state["stock"])

    # consider our options

    # only consider "do nothing" if one type is not available
    options = can_build( state, bp, 0 )
    # review options and cull do nothing if we can build ANY bot

    #must_build = True
    #for res in types:
        #build_this = False
        #for option in options:
            #if option["built"][res]:
                #build_this = True
                #break
        #if not build_this:
            #must_build = False
            #break
    #print("**** BUILD ALL")

    #if state["stock"]["ore"]>=bp["max_ore"] and state["bots"]["clay"]==0:
        #must_build = True


    # collect resources only after starting to build bots


    #pprint(options)
    best = 0
    for option in options:
        #if must_build and option["built"]["clay"]==False and option["built"]["ore"]==False and option["built"]["obsidian"]==False and option["built"]["geode"]==False:
                #print( "*** BUILDALL SKIP")
                #continue
        # update the new stock with the bots that existed at the start of the tick
        for res in state["bots"]:
            option["stock"][res] += state["bots"][res]
        sub_best = best_outcome( time+1, option, bp, indent=indent+f"{len(options)}/" )
        if sub_best>best:
            best=sub_best
    cache[code]=best
    return best


answer = 0
for bp in bps:
    cache={}
    print(f'***** {bp["number"]} ******')
    zero_state = { "bots":{"clay":0,"geode":0,"obsidian":0,"ore":1},
                   "stock":{"clay":0,"geode":0,"obsidian":0,"ore":0} }
#    zero_state = { "bots":{"clay":0,"geode":0,"obsidian":0,"ore":1},
#                   "stock":{"clay":10,"geode":0,"obsidian":0,"ore":10} }
    best = best_outcome( 0, zero_state, bp)
    print(best)
    quality = best * bp["number"]
    answer += quality


print( f'PART 1 = {answer}' )

