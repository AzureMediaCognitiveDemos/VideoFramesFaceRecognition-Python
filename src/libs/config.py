########### Python 2.7 #############
import sys
import os

def read_config(s):
    config = {}
    f = open(s)
    line = f.readline().strip()
    while line:
        #print line
        line = f.readline().strip()
        # skip if line start from sharp
        if line[0:1] == '#':
            continue
        arrs=line.split('=',1)
        if len(arrs) != 2:
            continue
        config[arrs[0]] = arrs[1]
    f.close
    return config


