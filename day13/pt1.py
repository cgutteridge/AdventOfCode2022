#!/usr/bin/python3

import sys
from pprint import pprint,pformat

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'
if( len(sys.argv) == 2  and sys.argv[1] == '-t2'):
    file = 'test2'

with open(file, 'r') as f:
	lines = f.read().split("\n")


def parse_value( chars ):
    # either a list with zero or more elements
    # or an integer
    # chars -1 is the next character  to consume
    if chars[-1] == '[':
        chars.pop() # consume [
        if chars[-1] == ']':
            # empty list!
            chars.pop() # consume ]
            return []
        r = [ parse_value( chars ) ]
        while chars[-1]==",":
            chars.pop() # consume ,
            r.append( parse_value( chars ) )
        # check
        if chars[-1] != ']':
            print( "ERROR, expected ']'")
            pprint(r)
            pprint(chars)
            exit()
        chars.pop() # consume ]
        return( r )
    if chars[-1] >= "0" and chars[-1] <= "9":
        nstr = ""
        while chars[-1] >= "0" and chars[-1] <= "9":
            nstr += chars[-1]
            chars.pop() # consume digit
        return int(nstr)

    print("unexpected char in parse value")
    pprint(chars)
    exit()

def parse_line( line ):
    chars = list(line)
    chars.reverse()
    #print()
    #print( "parse line" )
    #print( line )
    p = parse_value( chars )
    return( p )


# 1 means correct order
# -1 means wrong
# 0 means no opinion
def compare_lists(a,b, indent=""):
    #print( indent+"COMPARE "+ pformat(a)+ " vs "+pformat(b) )



    #print( "SAME LENGTH LISTS" )
    for i in range(0,len(a)):
        if i==len(b):
            #print( indent+" b ran out first : -1" )
            #print( indent+" longer : -1" )
            return -1

        # consider each pair in this list
        left = a[i]
        right = b[i]
        #print( indent+"  COMPARE LISTITEM "+ pformat(left)+ " vs "+pformat(right) )
        if type(left)==int and type(right)==int:
            if left < right:
                #print( indent+"  right int bigger: 1" )
                return 1
            if left > right:
                #print( indent+"  left int bigger: -1" )
                return -1
            # both the same, continue
            continue
        # convert to lists if needed
        if type(left)==int:
            left = [left]
        if type(right)==int:
            right = [right]
        pair_v = compare_lists(left, right, indent=indent+"   ")
        if pair_v != 0:
            return pair_v

    if len(a)<len(b):
        #print( indent+" a ran out first : 1" )
        return 1
    return 0

#[1,[2,[3,[4,[5,6,7]]]],8,9]
#[1,[2,[3,[4,[5,6,0]]]],8,9]
pairs = []
line_number = 0
while line_number<len(lines):
    if lines[line_number] == "":
        line_number+=1
        continue
    l1 = parse_line(lines[line_number])
    l2 = parse_line(lines[line_number+1])
    pairs.append( [l1,l2] )
    line_number+=2

pt1 = 0
for pair_index in range(0,len(pairs)):
    pair = pairs[pair_index]
    print()
    pprint(pair)
    r = compare_lists(pair[0],pair[1])
    print(r)
    if r==1:
        pt1+=pair_index+1

print( f'PART 1 = {pt1}' )


