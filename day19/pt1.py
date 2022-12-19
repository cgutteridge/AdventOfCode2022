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
    bp["max_geode"]=23
    bp["max_obsidian"]= bp["max_geode"]-1
    s = bp["rec"]["geode"]["obsidian"]
    i = 1
    while( s>0 ):
        s-=i
        bp["max_obsidian"]-=1
        i+=1
    bp["max_clay"]= bp["max_obsidian"]-1
    s = bp["rec"]["obsidian"]["clay"]
    i = 1
    while( s>0 ):
        s-=i
        bp["max_clay"]-=1
        i+=1
    bps.append(bp)

pprint(bps)

# {'number': '2',
#  'rec': {'clay': {'ore': 3},
#          'geode': {'obsidian': 12, 'ore': 3},
#          'obsidian': {'clay': 8, 'ore': 3},
#          'ore': {'ore': 2}}}]

types= ["ore","clay","obsidian","geode" ]


cache = {}
hits = 0
its = 0
meho = 0
mehc = 0

def best_outcome( time, state, bp, indent="", r=""):
    global mehc
    global meho
    global its
    global hits
    global cache
    if time==25:
        state["r"]=r
        return state
    if time>bp["max_obsidian"] and state["bots"]["obsidian"]==0:
        #print("MEH OBSIDIAN")
#        if meho % 10000 == 0:
#            print( f"MEH OBSIDIAN : {meho}")
#        meho+=1
        return state
    if time>bp["max_clay"] and state["bots"]["clay"]==0:
        #print("MEH CLAY")
#        mehc+=1
#        if mehc % 10000 == 0:
#            print( f"MEH CLAY : {mehc}")
        return state

    code=f'{time},{state["bots"]["ore"]},{state["bots"]["clay"]},{state["bots"]["obsidian"]},{state["bots"]["geode"]},{state["stock"]["ore"]},{state["stock"]["clay"]},{state["stock"]["obsidian"]},{state["stock"]["geode"]}'
    its+=1
    if code in cache:
        #hits+=1
        #if hits%10000==0:
            #print( f"CDING! {hits}/{its}={hits/its}" )
        return cache[code]
    if time==7:
        #print("YAY")
        print(indent+f' time={time} {code} {timecheck()} cache={len(cache)} ')
    #pprint(state["stock"])

    # consider our options
    options = ["NULL"]
    can_geode=False
    for res in types:
        can_buy = True
        for cost_res in bp["rec"][res]:
            if state["stock"][cost_res]<bp["rec"][res][cost_res]:
                can_buy = False
                break
        if can_buy:
            options.append(res)
            if res == 'geode':
                can_geode=True
    if can_geode:
        options=["geode"]

    # collect resources
    for res in state["bots"]:
        state["stock"][res] += state["bots"][res]

    #pprint(options)

    best = None
    for i in range(0,len(options)):
        option=options[i]
        new_state = {"bots":dict(state["bots"]),"stock":dict(state["stock"])}
        if option != "NULL":
            new_state["bots"][option]+=1
            for cost_res in bp["rec"][option]:
                new_state["stock"][cost_res] -= bp["rec"][option][cost_res]
        st = new_state["stock"]
        rc = f'{time} {option} {st["ore"]}o {st["clay"]}c {st["obsidian"]}ob {st["geode"]}g'
        sub_best = best_outcome( time+1, new_state, bp, indent=indent+f"{i+1}/{len(options)}:", r=r+rc+"\n")
        if best==None or sub_best["stock"]["geode"]>best["stock"]["geode"]:
            best=sub_best
    cache[code]=best
    return best

answer = 0
for bp in bps:
    cache = {}
    print(f'***** {bp["number"]} ******')
    zero_state = { "bots":{"clay":0,"geode":0,"obsidian":0,"ore":1},
                   "stock":{"clay":0,"geode":0,"obsidian":0,"ore":0} }
#    zero_state = { "bots":{"clay":0,"geode":0,"obsidian":0,"ore":1},
#                   "stock":{"clay":10,"geode":0,"obsidian":0,"ore":10} }
    pprint(bp)
    best = best_outcome( 1, zero_state, bp)
    answer += best["stock"]["geode"] * bp["number"]
    pprint(best)

                  



print( f'PART 1 = {answer}' )

