# -*- coding: utf-8 -*-
"""
stackFiles.py
~~~~~~~~~~

This script stacks multiple text files into a single text file (.txt).

Input: 1) Path of text file(s) to stack as a single file
       2) Name of output stack text file

Output: A stacked text file.

Usage:  $ python stackFiles.py './written_morphed_utf8' 'stack.txt'

Yejin Cho (scarletcho@gmail.com)
Last updated: 2016-12-06
"""
import os, sys, glob

path = sys.argv[1]
stackfname = sys.argv[2]

os.chdir(path)
flist = glob.glob("*.txt")

with open(stackfname, 'w') as outfile:
    for fname in flist:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
