#!/usr/bin/python3

import sys
from pprint import pprint

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'

with open(file, 'r') as f:
	lines = f.read().split("\n")
########################################
def print_stacks(stacks):
    max_height = 0
    for stack in stacks:
        if len(stack)>max_height:
            max_height=len(stack)
    for y in range(max_height,0,-1):
        blocks = []
        for x in range(0,len(stacks)):
            stack = stacks[x]
            if len(stack)>= y:
                blocks.append(f"[{stack[y-1]}]")
            else:
                blocks.append("   ")
        print( " ".join(blocks) )
    print()

########################################

index = 0
stacks = []
while lines[index] != "":
    chars = list(lines[index])
    index += 1
    if(chars[1]=="1"):
        continue
    row_size = int((len(chars)+1)/4)
    # row_size is consistant
    if len(stacks)==0:
        for c in range(0,row_size):
            stacks.append([])
    for c in range(0,row_size):
        block = chars[c*4+1]
        if block != " ":
            stacks[c].insert(0,block)
index += 1
orders = [];
while lines[index] != "":
    bits = lines[index].split( " " )
    orders.append( { "count":int(bits[1]), "from": int(bits[3])-1, "to": int(bits[5])-1 } )
    index += 1

print_stacks(stacks)
for order in orders:
    pprint(order)
    crane = []
    for i in range(0,order['count']):
        crane.append( stacks[order['from']].pop() )
    pprint( crane )
    for i in range(0,order['count']):
        stacks[order['to']].append(crane.pop())
    print_stacks(stacks)

# get the top item from each stack
top = []
for stack in stacks:
    top.append( stack[-1] )
pt1="".join(top)
        
print(f'PT1: {pt1}')
