# -*- coding: utf-8 -*-
"""
runkolm.py
~~~~~~~~~~

This is a sample wrapper for using kolm Python package.

Usage: $ python runkolm.py rawCorpusPath

Yejin Cho (scarletcho@gmail.com)

Last updated: 2017-02-22
"""


# datapath = '/Users/Scarlet_Mac/mydata/'

datapath = '/Users/Scarlet_Mac/mydata/'

import os
os.chdir(datapath)

os.system('rm -rf ./corpus/*')
os.makedirs('./corpus/raw')
os.makedirs('./corpus/encoded')
os.makedirs('./corpus/stack')

os.system('mv *.txt ./corpus/raw/')



# (1) Convert to UTF-8 encoding
from kolm.utils import *
convertEncoding('./corpus/raw/', 'utf-16', 'utf-8')

os.chdir(datapath)
os.system('mv ./corpus/raw/utf-8*.txt ./corpus/encoded/')
os.chdir(datapath + 'corpus/encoded')


# (2) Stack multiple text files into single file
from kolm.utils import *
stackFiles('.', 'headered_stack.txt')

os.chdir(datapath)
os.system('mv ./corpus/encoded/headered_stack.txt ./corpus/stack/')
os.chdir(datapath + 'corpus/stack')


# (3) Remove TEI header
from kolm.utils import *
removeHeader('headered_stack.txt')


# (4) Normalize text
from kolm.normalize import *
Knormalize('stack.txt', 'normalized.txt')


# (5) Morpheme analysis on raw text'
from kolm.tag import *
morphTag('normalized.txt', 'tagged.txt')

# morphTag 단계에서 Mecab 형태소분석 출력형태를 세종과 같은 형식으로 만들어야 제대로 작동 가능
# 세종 예:  원문 띄어쓰기를 유지하되 형태소 경계는 +로 표시. 다중 태그가 붙는 경우 없음.
#         (반면 Mecab은 다중 태그를 연결해버리는 차이 있음 유의)
#     조선일보/NNP 구십/NR+년__02/NNB 인터뷰/NNG+기사__10/NNG
#     박태준/NNP+외__04/NNB 기자__05/NNG+들__09/XSN
#     대한민국/NNP 문화__01/NNG+관광부/NNG
#     전자__06/NNG+표준화/NNG


# (6) Pseudo-morpheme analysis from raw & morpheme-tagged text
from kolm.tag import *
pseudomorph('normalized.txt', 'tagged.txt', 'classic')


# (7) Generate files for building LM (i.e. 'lexicon.txt', 'textraw')
from kolm.lm import *
writeTextraw('normalized.txt')
getUniqueWords('textraw')
writeLexicon('wordlist.txt')

