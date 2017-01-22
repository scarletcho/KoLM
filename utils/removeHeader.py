# -*- coding: utf-8 -*-
"""
removeHeader.py
~~~~~~~~~~

This script removes TEI header of a text file.

Input: 1) Path of text file to remove TEI headers from
       2) Name of input text file with TEI headers
       3) Name of output text file without any TEI header

Output: A TEI header removed text file.

Usage:  $ python removeHeader.py './written_morphed_utf8' 'stack_written_utf8.txt' 'noheader_stack_written_utf8.txt'

Yeonjung Hong (yvonne.yj.hong@gmail.com)
Yejin Cho (scarletcho@gmail.com)

Last updated: 2016-12-06
"""

import datetime as dt
import os
import re
import sys

path = sys.argv[1]
headeredfname = sys.argv[2]
noheaderfname = sys.argv[3]

# Set working directory
os.chdir(path)

# Mark beginning time
beg = dt.datetime.now()

# Regular expression pattern for extracting body text
# Unfortunately, since look-behind should have fixed width,
# unwanted tags in the beginning part of paragraph are extracted here.
pat2extract = (
    "(^.*?<l>.*?(?=</l>)|"
    "^.*?<p>.*?(?=</p>)|"
    "^.*?<q>.*?(?=</q>))").format()

# init for total line counts
total_count = 0

# Read headered text
with open(headeredfname, "r") as headeredtxt:
    body = []  # init body
    for line in headeredtxt:
        total_count += 1
        if re.findall(pat2extract, line):
            captured = re.findall(pat2extract, line)
            for l in captured:
                body.append(l)

# Patterns to delete after the first process
pat2del_1 = (
    "(</?l>|</?q>|</?text>|</?body>|</?def>|</?emph>|</?lg>|</?formula>|</?P>|</?poem>|"
    "<date>.*?</date>|<note>.*?</note>|<stage>.*?</stage>|<source>.*?</source>|"
    "<author>.*?</author>|<bibl>.*?</bibl>|<head>.*?</head>|<title>.*?</title>|<speaker>.*?</speaker>|"
    "<pb n.*?>|<lb n.*?>|<ph n.*?>|<gap desc.*?>|<gap reason.*?>)").format()

pat2del_2 = "(</?scnum>|</?sp>|</?sz>|</?set>|</?date>|</?head>|</?stage>|<stgae>)"

# Patterns to replace with a white space
pat2rep_1 = "</?p>"

# Patterns to replace due to typo in the original text
pat2rep_2 = "</formula\">"

# Typo list
# <ph n.*?>, <stgae>, </formula\">

# Write a new text with the remaining tags deleted
f = open(noheaderfname, "w")
for line in body:
    trimmed = re.sub(pat2del_1, '', line)
    trimmed = re.sub(pat2del_2, '', trimmed)
    trimmed = re.sub(pat2rep_1, ' ', trimmed)
    trimmed = re.sub(pat2rep_2, '"', trimmed)
    f.write("{}\n".format(trimmed))
f.close()

end = dt.datetime.now()
print(end-beg)
print("original line of text length: " + str(total_count))
print("Trimmed line of text length: " + str(len(body)))
