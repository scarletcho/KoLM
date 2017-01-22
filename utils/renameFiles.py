# -*- coding: utf-8 -*-
"""
renameFiles.py
~~~~~~~~~~

This script renames filename(s) in a given folder
according to given regexp input.

Input:  1) Path of the directory to investigate.
        2) Pattern to be substituted.
        3) Desired output substring.

Output: Renamed file(s) in the given path.

Yejin Cho (scarletcho@gmail.com)
Last updated: 2016-12-20
"""
import os
import glob
import re

def replaceSubstring(line, newstr, ituple):
    output = line[0:ituple[0]] + newstr + line[ituple[1]:]
    return output


def addNumber(path, addnum):
    os.chdir(path)
    flist = glob.glob("*")

    numlist = []

    for fname in flist:
        for numiter in re.finditer(u'\d+', fname):
            numlist.append(numiter.group())

        if len(numlist) > 0:
            for i in range(0, len(numlist)):
                # Re-initialize numidx & alphalist stack
                numidx = []
                numlist = []

                for numiter_fresh in re.finditer(u'\d+', fname):
                    numidx.append(numiter_fresh.span())
                    numlist.append(numiter_fresh.group())

                while len(numlist) > 0:
                    num = numlist[0]
                    break

                num = str(int(num) + addnum)

                ituple = numidx[0]
                numlist[0] = num
            newname = replaceSubstring(fname, num, ituple)
            print newname

            renameFile(fname, newname)


def renameFile(oldname, newname):
    os.rename(oldname, newname)


path = '/Users/Scarlet_Mac/PycharmProjects/KUcorpus/박상준/data_Kor'
addNumber(path, 1000)