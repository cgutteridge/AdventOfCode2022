#!/usr/bin/python3

import sys
from pprint import pprint

file = 'data'
if( len(sys.argv) == 2  and sys.argv[1] == '-t'):
    file = 'test'

with open(file, 'r') as f:
	lines = f.read().split("\n")

########################################

# assume we've done find_size
def dir_sizes( dir, path="", found={} ):
    for filename in dir:
        if( filename == ".." ):
            continue
        if( dir[filename]["type"] == "file" ):
            continue
        found[path+"/"+filename]=dir[filename]["size"]
        dir_sizes( dir[filename]["ref"], path=path+"/"+filename, found=found )
    return found

    

def find_size( dir ):
    size = 0
    for filename in dir:
        if( filename == ".." ):
            continue
        if( dir[filename]["type"] == "dir" and not dir[filename].get("size") ):
            dir[filename]["size"] = find_size( dir[filename]["ref"] )
        size += dir[filename]["size"]
    return size


def dir_r(dir, indent=""):
    for filename in dir:
        if( filename == ".." ):
            continue
        if( dir[filename]["type"] == "file" ):
            print( ""+indent + filename + " (" +str(dir[filename]["size"])+")" )
        else:
            if( dir[filename].get("size") ):
                print( ""+indent + filename + " (dir) (" +str(dir[filename]["size"])+")" )
            else:
                print( ""+indent + filename + " (dir)")
            dir_r( dir[filename]["ref"], indent=indent+"  " )

########################################

disk = {}
cwd = disk
i=0
while i < len(lines):
    cmd = lines[i]
    i += 1
    if cmd=="":
        continue
    args = cmd.split( " " )
    if( args[0] != "$" ):
        print( f"ERROR, unexpeced value at line {i}." )
        exit()
    if( args[1] == "cd" ):
        if( args[2]=="/" ):
            cwd = disk
            continue
        thing = cwd[args[2]]
        if( thing["type"] != "dir" ):
            print( f"ERROR, no such dir at line {i}." )
            exit()
        cwd = thing["ref"]
        continue
    if( args[1] != "ls" ):
        print( f"ERROR, unexpeced command at line {i}." )

    while( i<len(lines) and not lines[i].startswith("$") ):
        item = lines[i]
        i += 1
        if item=="":
            continue
        # size/dir name
        bits = item.split( " " )
        if( bits[0] == "dir" ):
            cwd[bits[1]] = {
                    "type":"dir",
                    "ref":{ "..":{"type":"dir", "ref":cwd} } }
        else:
            cwd[bits[1]] = {
                    "type":"file",
                    "size":int(bits[0])
                    }

total_used = find_size( disk )

print()
dir_r( disk )
print()

dirs = dir_sizes( disk )

pt1 = 0
for dirname in dirs:
    size = dirs[dirname]
    if(size < 100000 ):
        pt1+=size

print(f'PT1: {pt1}')

disk_size = 70000000

needed_free = 30000000

current_free = disk_size - total_used

delete_target = needed_free - current_free

print( delete_target )

# find the smallest dir bigger than delete target
pt2 = disk_size
for dirname in dirs:
    size = dirs[dirname]
    if( size < delete_target ):
        continue
    if( size < pt2 ):
        pt2 = size

print(f'PT2: {pt2}')
