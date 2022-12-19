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


# {'number': '2',
#  'rec': {'clay': {'ore': 3},
#          'geode': {'obsidian': 12, 'ore': 3},
#          'obsidian': {'clay': 8, 'ore': 3},
#          'ore': {'ore': 2}}}]

# in order of desirability
types= [
        "geode" ,
        "obsidian",
        "clay",
        "ore"
        ]

def best_outcome( bp ):
    # bot complete building times at end of this minute
    bot_times = {
            "ore":[0],
            #"ore":[0],
            "clay":[],
            "obsidian":[],
            "geode":[] }

    changed=True
    seen = {}

    # minute index is 0 
    while changed:
        code = ""
        for res_i in types:
            bot_times[res_i].sort()
            code += "/"+res_i+":"
            for bot_time in bot_times[res_i]:
                code += str(bot_time)+","
        state = [] # represents state at END of minute
        to_spend = [] # represents spending power in this minute (ie. after bots are paid for, before incs)
        can_build=[]
        for minute in range(0,25):
            stock = {}
            for res in types:
                stock[res]=0
            state.append(stock)
            to_spend_row = {}
            for res in types:
                to_spend_row[res]=0
            to_spend.append(to_spend_row)
            can_build.append(True)
    
        for bot_res in bot_times:
            for pmin in bot_times[bot_res]:
                can_build[pmin]=False
                for tick in range(pmin, 25):
                    state[tick][bot_res] += tick-pmin
                    if tick<24:
                        to_spend[tick+1][bot_res] += tick-pmin
                    # lower stock based on bot changed time
                    # but not for the starting bot
                    if pmin!=0:
                        for cost_res in bp["rec"][bot_res]:
                            state[tick][cost_res] -= bp["rec"][bot_res][cost_res]
                            to_spend[tick][cost_res] -= bp["rec"][bot_res][cost_res]

        print("-------------------")
        debug(bot_times,state,to_spend)



        for minute in range(0,25):
            for res in state[minute]:
                if state[minute][res]<0:
                    print( "OH DANG")
                    exit()
            

        changed=False
        for build_res in types:
            # see if we can move anything of this resource 1 minute earlier
            for i in range(0,len(bot_times[build_res])):
                bot_time = bot_times[build_res][i]

                earliest = bot_time
                earliest_allowed = bot_time
                check_minute = bot_time
                # if find from now upwards how far there are free spend points, build=False places can be 
                # skipped over but must still be checked for free resources
                while check_minute > 1:
                    check_minute = check_minute-1
                    for cost_res in bp["rec"][build_res]:
                        if to_spend[check_minute][cost_res]<bp["rec"][build_res][cost_res]:
                            # too poor
                            ok = False
                            break
                    if ok:
                        earliest = check_minute
                        if can_build[check_minute]:
                            earliest_allowed=check_minute
                if earliest_allowed != bot_time:
                        bot_times[build_res][i] = earliest_allowed
                        print(f'moved a {build_res} at {bot_time} forward to {bot_times[build_res][i]}')
                        changed = True
            if changed:
                break

            #print(f' Maybe {build_res}?')
            for build_minute in range(1,24):
                # don't build at time 24
                # don't build where a bot already is
                if not can_build[build_minute]:
                    continue

                # has resources?
                ok = True
                for cost_res in bp["rec"][build_res]:
                    # check state from now until the end of time as stealing resources here steals them from the future
                    for check_minute in range(build_minute,25):
                        if to_spend[check_minute][cost_res]<bp["rec"][build_res][cost_res]:
                            #print(f'cant build {build_res} at {build_minute} because {cost_res} {state[build_minute][cost_res]} < {bp["rec"][build_res][cost_res]} @ {check_minute}')
                            # too poor
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    # build a bot at this minute
                    bot_times[build_res].append(build_minute)
                    print(f'Added a {build_res} at {build_minute}')
                    # things have changed so don't keep the skip
                    changed= True
                    break
            if changed:
                break
            #print(f"can't build {build_res}")
        if not changed:
            # as a last ditch, see if any of the 

            for build_res in types:
                # see if this bot contributes nothing
                # geodes are always good
                if build_res=="geode":
                    continue
                for i in range(0,len(bot_times[build_res])):
                    bot_time = bot_times[build_res][i]
                    useless = True
                    for check_t in range(bot_time,25):
                        if to_spend[check_t][build_res]<check_t-bot_time:
                            # I guess it's needed
                            useless=False
                        
                    if useless:
                        code += f':{build_res},{bot_time}'
                        if code in seen:
                            continue
                        seen[code]=True
                        print(code)
                        # it's contribution isn't used
                        print(f'Killed a stupid {build_res} bot at {bot_time}')
                        del bot_times[build_res][i]
                        changed = True
                        # ban adding it back right away
                        break
                if changed:
                    break
        # end of While changed loop
    debug(bot_times,state,to_spend)
    print("LAST")
    return state[24]["geode"]

def debug(bot_times,state,to_spend):
    pprint( bot_times)
    for minute in range(0,25):
        sm=state[minute]
        sp=to_spend[minute]
        botlist=[]
        for bot_res in bot_times:
            for pmin in bot_times[bot_res]:
                if pmin==minute:
                    botlist.append(bot_res)
        print(f'{str(minute).rjust(2)} {str(sm["ore"]).rjust(2)}o {str(sm["clay"]).rjust(2)}c {str(sm["obsidian"]).rjust(2)}b {str(sm["geode"]).rjust(2)}g TOSPEND: {str(sp["ore"]).rjust(2)}o {str(sp["clay"]).rjust(2)}c {str(sp["obsidian"]).rjust(2)}b {str(sp["geode"]).rjust(2)}g {",".join(botlist)}')

answer = 0
first = True
for bp in bps:
    if first:
        first=False
        #continue
    print(f'***** {bp["number"]} ******')
    pprint(bp)
    best = best_outcome( bp)
    pprint(bp)
    print(best)
    quality = best * bp["number"]
    answer += quality


print( f'PART 1 = {answer}' )

