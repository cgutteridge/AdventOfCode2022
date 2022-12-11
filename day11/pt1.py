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

cft = []
for i in range(0, len(lines), 7 ):
    m = {}
    a = lines[i+1].split( ": " )
    m["items"] = []
    for v in a[1].split(", "):
        m["items"].append(int(v))
    b = lines[i+2].split( " " )
    m["op_left"] = b[5]
    m["op_op"] = b[6]
    m["op_right"] = b[7]
    c = lines[i+3].split( " " )
    m["test"] = int(c[5])
    d = lines[i+4].split( " " )
    m["iftrue"] = int(d[9])
    e = lines[i+5].split( " " )
    m["iffalse"] = int(e[9])
    m["inspected"]=0
    cft.append(m)

pt1 = 0


for round in range(0,20):
    for m_i in range(0,len(cft)):
        #print(f'MONKEY {m_i}')
        m = cft[m_i]
        #pprint(m)
        for item in m["items"]:
            # inspect
            m["inspected"]+=1
            #pprint(item)
            if m["op_left"]=="old":
                l1 = item
            else:
                l1 = int(m["op_left"])
            if m["op_right"]=="old":
                l2 = item
            else:
                l2 = int(m["op_right"])
            if m["op_op"]=="+":
                v=l1+l2
                #print(f'{l1}+{l2} = {v}')
            else:
                #assume *
                v=l1*l2
                #print(f'{l1}*{l2} = {v}')
            v = int(v/3)
            #print(f'bored {v}')
            if v % m["test"] == 0:
                #print( "TRUE=>")
                #print( m["iftrue"] )
                cft[m["iftrue"]]["items"].append( v )
            else:
                #print( "FALSE=>")
                #print( m["iffalse"] )
                cft[m["iffalse"]]["items"].append( v )
        # monkey now has no items
        m["items"]=[]

scores = []
for m in cft:
    scores.append(m["inspected"])

scores.sort(reverse=True)
pprint(scores)
pt1=scores[0]*scores[1]
#Monkey 0:
  #Starting items: 79, 98
  #Operation: new = old * 19
  #Test: divisible by 23
    #If true: throw to monkey 2
    #If false: throw to monkey 3


print(f'PT1: {pt1}')

