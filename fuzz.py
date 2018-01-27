#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 00:22:41 2018

@author: w
"""

import sys, random

if len(sys.argv) != 3:
    sys.exit('Usage: %s file_name num_bitflips' % sys.argv[0])
    
with open(sys.argv[1], "rb") as f:
    contents = f.read()
    l = len(contents)
contents = bytearray(contents)

for i in range(int(sys.argv[2])):
    r = random.randint(0, l-1)
    contents[r] ^= 1
    
with open(sys.argv[1], "wb") as f:
    f.write(contents)