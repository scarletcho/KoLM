# -*- coding: utf-8 -*-
"""
prepLM.py
~~~~~~~~~~

This script generates textraw file for Kaldi LM from pseudo-morpheme tagged corpus.

Input: Pseudo-morpheme tagged corpus (filename)

Output: textraw
        lexicon.txt


Yejin Cho (scarletcho@gmail.com)

Last updated: 2016-12-27
"""

import os
import sys
from konlpy.utils import pprint
import re
import g2p

reload(sys)
sys.setdefaultencoding('utf-8')


def readfileUTF8(fname):
    f = open(fname, 'r')
    corpus = []

    while True:
        line = f.readline()
        line = unicode(line.encode("utf-8"))
        line = re.sub(u'\n', '', line)
        if line != u'':
            corpus.append(line)
        if not line: break

    f.close()
    return corpus


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

        if not line.isspace():  # Space check
            if line:  # Emptiness check
                body.append(unicode(line))

    return body


def boundary2space(corpus):
    # Morpheme-boundaries into spaces
    body = []
    for lines in corpus:
        lines = re.sub(u'\+', u' ', lines)
        body.append(lines)
    return body


def writefile(body, fname):
    out = open(fname, 'w')
    for line in body:
        out.write('{}\n'.format(line))
    out.close()


def writeTextraw(corpus):
    body = boundary2space(corpus)
    body = tightenString(body)
    writefile(body, 'textraw')

    return body


def getUniqueWords(corpus):
    uqlist = []
    idx = 0
    for line in corpus:
        print('line #: ' + str(idx))
        wordlist = line.split()
        for word in wordlist:
            if not word.isspace():  # Space check
                if word:  # Emptiness check
                    uqlist.append(unicode(word))
        idx += 1
    uqlist = list(set(uqlist))

    return uqlist


def writeLexicon(uqlist):
    lexicon = []
    idx = 0
    for item in uqlist:
        print('line #: ' + str(idx))
        try:
            prono = g2p.graph2prono(item, 'rules_g2p.xls')
            prono_spaced = ''
            idx2take = range(0, len(prono) + 2, 2)

            for n in range(0, len(idx2take) - 1):
                if n < len(idx2take) - 2:
                    prono_spaced = prono_spaced + prono[idx2take[n]:idx2take[n + 1]] + ' '
                else:  # When final two letters reached
                    prono_spaced = prono_spaced + prono[idx2take[n]:idx2take[n + 1]]

            lexicon.append(item + u' ' + prono_spaced)

        except:
            print(item)
        idx += 1

    writefile(lexicon, 'lexicon.txt')
    return lexicon



corpus = readfileUTF8('textraw')
# body = writeTextraw(corpus)
uq = getUniqueWords(corpus)
lexicon = writeLexicon(uq)

