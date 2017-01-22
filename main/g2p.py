# -*- coding: utf-8 -*-
'''
g2p.py
~~~~~~~~~~

This script converts Korean graphemes to romanized phones and then to pronunciation.

  (1) graph2phone(graphs): convert Korean graphemes to romanized phones
  (2) phone2prono(phones): convert romanized phones to pronunciation


Jaegu Kang (jaekoo.jk@gmail.com)
Hyungwon Yang (hyung8758@gmail.com)
Yeonjung Hong (yvonne.yj.hong@gmail.com)
Yejin Cho (scarletcho@gmail.com)

Created: 2016-08-11
Last updated: 2016-12-27 Yejin Cho
'''


import re
import math
import xlrd
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def getRulebook(rulefname):
    try:
        rule_book = xlrd.open_workbook(rulefname)
    except IOError:
        print('\nrules_g2p.xls does not exist or is corrupted')
        print('\nLocate rules_g2p.xls in the same folder as in g2p.py')

    return rule_book


def readRules(rule_book):
    # read rules_g2p.xls
    rule_sheet = rule_book.sheet_by_name(u'ruleset')
    var = rule_sheet.cell(0, 0).value

    rule_in = []
    rule_out = []
    for idx in range(0, rule_sheet.nrows):
        rule_in.append(rule_sheet.cell(idx, 0).value)
        rule_out.append(rule_sheet.cell(idx, 1).value)

    return rule_in, rule_out


def isHangul(charint):
    hangul_init = 44032
    hangul_fin = 55203
    return charint >= hangul_init and charint <= hangul_fin


def checkCharType(var_list):
    #  1: whitespace
    #  0: hangul
    # -1: non-hangul
    checked = []
    for i in range(len(var_list)):
        if var_list[i] == 32:   # whitespace
            checked.append(1)
        elif isHangul(var_list[i]): # Hangul character
            checked.append(0)
        else:   # Non-hangul character
            checked.append(-1)
    return checked


def graph2phone(graphs):
    # Encode graphemes as utf8
    graphs = graphs.decode('utf8')
    integers = []
    for i in range(len(graphs)):
        integers.append(ord(graphs[i]))

    # Romanization (according to Korean Spontaneous Speech corpus; 성인자유발화코퍼스)
    phones = ''
    ONS = ['k0', 'kk', 'nn', 't0', 'tt', 'rr', 'mm', 'p0', 'pp',
           's0', 'ss', 'oh', 'c0', 'cc', 'ch', 'kh', 'th', 'ph', 'hh']
    NUC = ['aa', 'qq', 'ya', 'yq', 'vv', 'ee', 'yv', 'ye', 'oo', 'wa',
           'wq', 'wo', 'yo', 'uu', 'wv', 'we', 'wi', 'yu', 'xx', 'xi', 'ii']
    COD = ['', 'kf', 'kk', 'ks', 'nf', 'nc', 'nh', 'tf',
           'll', 'lk', 'lm', 'lb', 'ls', 'lt', 'lp', 'lh',
           'mf', 'pf', 'ps', 's0', 'ss', 'oh', 'c0', 'ch',
           'kh', 'th', 'ph', 'hh']

    # Pronunciation
    idx = checkCharType(integers)
    iElement = 0
    while iElement < len(integers):
        if idx[iElement] == 0:  # not space characters
            base = 44032
            df = int(integers[iElement]) - base
            iONS = int(math.floor(df / 588)) + 1
            iNUC = int(math.floor((df % 588) / 28)) + 1
            iCOD = int((df % 588) % 28) + 1

            s1 = '-' + ONS[iONS - 1]  # onset
            s2 = NUC[iNUC - 1]  # nucleus

            if COD[iCOD - 1]:  # coda
                s3 = COD[iCOD - 1]
            else:
                s3 = ''
            tmp = s1 + s2 + s3
            phones = phones + tmp
        elif idx[iElement] == 1:  # space character
            tmp = ' '
            phones = phones + tmp
        phones = re.sub('-(oh)', '-', phones)
        iElement += 1
        tmp = ''

    # Final velar nasal
    phones = re.sub('^oh', '', phones)
    phones = re.sub('-(oh)', '', phones)
    phones = re.sub('oh-', 'ng-', phones)
    phones = re.sub('oh$', 'ng', phones)
    phones = re.sub('oh ', 'ng ', phones)

    phones = re.sub('(\W+)\-', '\\1', phones)
    phones = re.sub('\W+$', '', phones)
    phones = re.sub('^\-', '', phones)
    return phones


def phone2prono(phones, rule_in, rule_out):
    # Apply g2p rules
    for pattern, replacement in zip(rule_in, rule_out):
        phones = re.sub(pattern, replacement, phones)
        prono = phones
    return prono


def graph2prono(graphs, rulefname):
    rule_book = getRulebook(rulefname)
    [rule_in, rule_out] = readRules(rule_book)

    romanized = graph2phone(graphs)
    pronunciation = phone2prono(romanized, rule_in, rule_out)

    return pronunciation



# Usage example:
# prono = graph2prono(u'한두 번 도 아니고', 'rules_g2p.xls')
# print(prono)
