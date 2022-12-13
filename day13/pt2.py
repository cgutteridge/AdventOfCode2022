#!/usr/bin/python3

import sys
from pprint import pprint,pformat
from functools import cmp_to_key

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

def cmp(a,b):
    return -compare_lists(a,b)

#[1,[2,[3,[4,[5,6,7]]]],8,9]
#[1,[2,[3,[4,[5,6,0]]]],8,9]
lists = [
[[2]],
[[6]]
        ]
for line in lines:
    if line == "":
        continue
    lists.append( parse_line( line ) )
lists.sort(key=cmp_to_key(cmp))
pprint( lists )


for i in range(0,len(lists)):
    if( compare_lists( [[2]], lists[i] )==0 ):
        i1=i+1
    if( compare_lists( [[6]], lists[i] )==0 ):
        i2=i+1
    

pt2 = i1*i2
print( f'PART 2 = {i1}x{i2} = {pt2}' )


