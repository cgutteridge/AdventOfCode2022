#!/usr/bin/python3

with open('data', 'r') as f:
	lines = f.read().split("\n")

dict = {
        "A X": 3, # Z
        "B X": 1, # X
        "C X": 2, # Y

        "A Y": 4, # X
        "B Y": 5, # Y
        "C Y": 6, # Z

        "A Z": 8, # Y
        "B Z": 9, # Z
        "C Z": 7, # X
        }
pt2 = 0;
for line in lines:
    if line == "":
        continue
    score = dict[line]
    pt2 += score

print(f'PT2: {pt2}')


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
