# -*- coding: utf-8 -*-
"""
lm.py
~~~~~~~~~~

This script generates textraw file for Kaldi LM from pseudo-morpheme tagged corpus.

Input: Pseudo-morpheme tagged corpus (filename)

Output: textraw
        lexicon.txt

Yejin Cho (scarletcho@gmail.com)


[NOTE] Please download the required python packages via pip command:
        KoNLPy ($ pip install JPype1
                $ pip install konlpy)

Last updated: 2017-02-22
"""

import os
import sys
import re
import site
from . import g2p

from konlpy.utils import pprint
from . import utils


# Check Python version
ver_info = sys.version_info
path = site.getsitepackages()[0]
[rule_in, rule_out] = g2p.readRules(ver_info[0], path + '/kolm/rulebook.txt')

if ver_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


def boundary2space(corpus):
    # Morpheme-boundaries into spaces
    body = []
    for lines in corpus:
        lines = re.sub(u'\+', u' ', lines)
        body.append(lines)
    return body


def writeTextraw(corpus):
    body = utils.readfileUTF8(corpus)
    body = boundary2space(body)
    body = utils.tightenString(body)

    utils.writefile(body, 'textraw')


def getUniqueWords(text_fname):
    corpus = utils.readfileUTF8(text_fname)
    uqlist = []
    idx = 0
    for line in corpus:
        print('line #: ' + str(idx))
        wordlist = line.split()
        for word in wordlist:
            if not word.isspace():  # Space check
                if word:  # Emptiness check
                    if sys.version_info[0] == 2:
                        uqlist.append(unicode(word))
                    else:
                        uqlist.append(word)
        idx += 1
    uqlist = list(set(uqlist))

    utils.writefile(uqlist, 'wordlist.txt')


def writeLexicon(text_fname):
    uqlist = utils.readfileUTF8(text_fname)
    lexicon = []
    idx = 0
    for graph in uqlist:
        print('line #: ' + str(idx))
        try:
            if ver_info[0] == 2:
                prono = g2p.graph2prono(unicode(graph), rule_in, rule_out)
            elif ver_info[0] == 3:
                prono = g2p.graph2prono(graph, rule_in, rule_out)

            lexicon.append(graph + ' ' + prono)
        except:
            print('Error: ' + graph)

        idx += 1

    utils.writefile(lexicon, 'lexicon.txt')

