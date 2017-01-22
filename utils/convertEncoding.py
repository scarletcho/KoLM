# -*- coding: utf-8 -*-
"""
convertEncoding.py
~~~~~~~~~~

This script converts encoding of text file(s) (*.txt).

Input: 1) Encoding of input text file (ex: 'utf-16')
       2) Encoding of desired output text file (ex: 'utf-8')
       3) Path of text file(s) of which you want to convert encoding
       4) [Optional] Name of a single text file
          (If not specified, conversion is applied to every text file in the specified directory.)

Output: Encoding converted text file(s)

Usage:  $ python convertEncoding.py 'utf-16' 'utf-8' './written_morphed'
        $ python convertEncoding.py 'utf-16' 'utf-8' './written_morphed' 'BTAA0001.txt'

Yejin Cho (scarletcho@gmail.com)
Last updated: 2016-12-06
"""
import os, sys, glob, re

encodingSource = sys.argv[1]
encodingDest = sys.argv[2]
path = sys.argv[3]

os.chdir(path)

if len(sys.argv) == 3:
    flist = glob.glob("*.txt")
elif len(sys.argv) > 3:
    flist = sys.argv[4]


if type(flist) is list:
    for i in range(0,len(flist)):
        txtname = flist[i]
        txtname = re.sub('\n','',txtname)

        fnameSource = txtname[0:len(txtname)]
        fnameDest = encodingDest + txtname[0:len(txtname)]

        # Convert encoding
        with open(fnameSource, 'rb') as fileSource:
            with open(fnameDest, 'w+b') as fileDest:
                contents = fileSource.read()

                # Write new files with desired encoding
                fileDest.write(contents.decode(encodingSource).encode(encodingDest))

elif isinstance(flist, basestring):
    print('This is Char!!')
    # txtname = flist
    # fnameSource = txtname[0:len(txtname)]
    # fnameDest = encodingDest + txtname[0:len(txtname)]
    #
    # # Convert encoding
    # with open(fnameSource, 'rb') as fileSource:
    #     with open(fnameDest, 'w+b') as fileDest:
    #         contents = fileSource.read()
    #
    #         # Write new files with desired encoding
    #         fileDest.write(contents.decode(encodingSource).encode(encodingDest))
