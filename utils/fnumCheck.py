# -*- coding: utf-8 -*-
"""
fnumCheck.py
~~~~~~~~~~

This script checks if filenames in a given folder are correctly numbered
without any overlap or leaping.

Input:  Path of the directory to investigate.
Output: Overlapping or missing file number(s).

Yejin Cho (scarletcho@gmail.com)
Last updated: 2016-12-20
"""
import os, glob, re
from collections import Counter


def check(path):
    fnumlist = getFileList(path)
    getDuplicates(fnumlist)
    getMissings(fnumlist)


def getFileList(path):
    os.chdir(path)

    flist = glob.glob("*")
    fnumlist = []

    for fname in flist:
        fnum = re.findall(u'\d+', fname)
        fnumlist.append(int(fnum[0]))
    print ('Total #: ' + str(len(fnumlist)))
    return fnumlist


def getDuplicates(fnumlist): # Print duplicated values
    print('Duplicates:')
    print([k for k, dup in Counter(fnumlist).items() if dup > 1])


def getMissings(fnumlist):  # Print missing values
    init = min(fnumlist)  # ex: 1
    fin = max(fnumlist)  # ex: 1800
    missing_values = []

    for i in range(init, fin):
        if not i in fnumlist:
            missing_values.append(i)
    print('Missing:')
    print(missing_values)


# Sample usage:
path = '/Users/Scarlet_Mac/PycharmProjects/KUcorpus/XU ZHENDONG'
check(path)
