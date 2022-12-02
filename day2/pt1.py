#!/usr/bin/python3

with open('data', 'r') as f:
	lines = f.read().split("\n")

dict = {
        "A X": 4,
        "B X": 1,
        "C X": 7,
        "A Y": 8,
        "B Y": 5,
        "C Y": 2,
        "A Z": 3,
        "B Z": 9,
        "C Z": 6,
        }
pt1 = 0;
for line in lines:
    if line == "":
        continue
    score = dict[line]
    pt1 += score

print(f'PT1: {pt1}')


#	if( line == "" ):
#		if( current_elf != -1 ):
#			elves.append( current_elf )
#		current_elf = 0
#		continue
#	current_elf += int(line)
#
#max_elf = 0
#for elf in elves:
#    if( elf > max_elf ):
#        max_elf=elf
#
#
#elves.sort(reverse=True)
#
#top3 = elves[0]+elves[1]+elves[2]
#
#print(f'PT2: {top3}')
