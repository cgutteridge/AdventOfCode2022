#!/usr/bin/python3

with open('data', 'r') as f:
	lines = f.read().split("\n")

elves = []
current_elf = -1
for line in lines:
	if( line == "" ):
		if( current_elf != -1 ):
			elves.append( current_elf )
		current_elf = 0
		continue
	current_elf += int(line)

max_elf = 0
for elf in elves:
    if( elf > max_elf ):
        max_elf=elf

print(f'PT1: {max_elf}')

elves.sort(reverse=True)

top3 = elves[0]+elves[1]+elves[2]

print(f'PT2: {top3}')
