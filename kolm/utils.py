# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~~~

This module includes useful methods for text managements for language models.

*** List of Methods:
    - convertEncoding(path, encodingSource, encodingDest, flist=[])
    - stackFiles(path, stackFname, flist=[])
    - tightenString(corpus)
    - getEojeolList(sentlist)
    - removeHeader(headeredfname)
    - readfileUTF8(fname)
    - writefile(body, fname)


[NOTE] Please download the required python packages via pip command:
        KoNLPy ($ pip install JPype1
                $ pip install konlpy)
        hanja  ($ pip install hanja)

Yejin Cho (scarletcho@gmail.com)

Last updated: 2017-02-22
"""

import os
import sys
import re
import glob
from konlpy.utils import pprint


# Check Python version
ver_info = sys.version_info

if ver_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

            
def convertEncoding(path, encodingSource, encodingDest, flist=[]):
    os.chdir(path)

    if len(flist) == 0:
        flist = glob.glob('*.txt')
    elif isinstance(flist, str):
        flist = [flist]

    if type(flist) is list:
        for i in range(0,len(flist)):
            txtname = flist[i]
            txtname = re.sub('\n','',txtname)

            fnameSource = txtname[0:len(txtname)]
            fnameDest = encodingDest + '_' + txtname[0:len(txtname)]

            # Convert encoding
            with open(fnameSource, 'rb') as fileSource:
                with open(fnameDest, 'w+b') as fileDest:
                    contents = fileSource.read()

                    # Write new files with desired encoding
                    fileDest.write(contents.decode(encodingSource).encode(encodingDest))


def stackFiles(path, stackFname, flist=[]):
    os.chdir(path)

    if len(flist) == 0:
        flist = glob.glob('*.txt')
    elif isinstance(flist, str):
        flist = [flist]

    with open(stackFname, 'w') as outfile:
        for fname in flist:
            with open(fname) as infile:
                for line in infile:
                    # Add a newline before concatenating files (if line break doesn't exists)
                    if line[-1] != '\n':
                        line = line + '\n'
                    outfile.write(line)


def tightenString(corpus):
    body = []  # init body
    for line in corpus:
        # Remove initial/final spaces surrounding given string
        line = re.sub(u'^\s+', u'', line)
        line = re.sub(u'\s+$', u'', line)

        # Remove spaces before sentence final punctuations
        line = re.sub(u'\s+\.', u'.', line)
        line = re.sub(u'\s+\!', u'!', line)
        line = re.sub(u'\s+\?', u'?', line)

        # Replace multiple spaces with a single space
        line = re.sub(u'[ \t]+', u' ', line)
        line = re.sub(u'^\n$', u'', line)

        if not line.isspace():  # Space check
            if line:  # Emptiness check
                if ver_info[0] == 2:
                    body.append(unicode(line))
                else:
                    body.append(line)

    return body


def getEojeolList(sentlist):
    output_stack = []

    for sent_id in range(0, len(sentlist)):
        sent = sentlist[sent_id]
        eojeol_list = sent.split(' ')
        output_stack.append(eojeol_list)

    return output_stack


def removeHeader(headeredfname):
    # (1) Regular expression patterns to extract
    pat2extract = ('(^.*?<l>.*?(?=</l>)|^.*?<p>.*?(?=</p>)|^.*?<q>.*?(?=</q>))')

    # (2) Patterns to delete after the first process
    pat2del_1 = (
        '(</?l>|</?q>|</?text>|</?body>|</?def>|</?emph>|</?lg>|</?formula>|</?P>|</?poem>|'
        '<date>.*?</date>|<note>.*?</note>|<stage>.*?</stage>|<source>.*?</source>|'
        '<author>.*?</author>|<bibl>.*?</bibl>|<head>.*?</head>|<title>.*?</title>|<speaker>.*?</speaker>|'
        '<pb n.*?>|<lb n.*?>|<ph n.*?>|<gap desc.*?>|<gap reason.*?>)').format()

    pat2del_2 = '(</?scnum>|</?sp>|</?sz>|</?set>|</?date>|</?head>|</?stage>|<stgae>)'

    # (3) Patterns to replace with a whitespace
    pat2rep_1 = '</?p>'

    # (4) Patterns to replace due to typo in the original text (cf. Sejong 21st corpus)
    pat2rep_2 = '</formula\">'


    # init for total line counts
    total_count = 0

    # Read headered text
    with open(headeredfname, 'r') as headeredtxt:
        body = []  # init body
        for line in headeredtxt:
            total_count += 1
            if re.findall(pat2extract, line):
                captured = re.findall(pat2extract, line)
                for l in captured:
                    body.append(l)

    # Write a new text with the remaining tags deleted
    with open('stack.txt', "w") as noheadertxt:
        for line in body:
            trimmed = re.sub(pat2del_1, '', line)
            trimmed = re.sub(pat2del_2, '', trimmed)
            trimmed = re.sub(pat2rep_1, ' ', trimmed)
            trimmed = re.sub(pat2rep_2, '"', trimmed)
            noheadertxt.write("{}\n".format(trimmed))
        noheadertxt.close()

    print("original line of text length: " + str(total_count))
    print("Trimmed line of text length: " + str(len(body)))


def readfileUTF8(fname):
    f = open(fname, 'r')
    corpus = []

    while True:
        line = f.readline()
        if ver_info[0] == 2:
            line = unicode(line.encode("utf-8"))
            line = re.sub(u'\n', u'', line)
        elif ver_info[0] == 3:
            line = re.sub('\n', '', line)
        if line != u'':
            corpus.append(line)
        if not line: break

    f.close()
    return corpus


def writefile(body, fname):
    out = open(fname, 'w')
    for line in body:
        out.write('{}\n'.format(line))
    out.close()

