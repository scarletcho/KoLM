# -*- coding: utf-8 -*-
"""
countEojeol.py
~~~~~~~~~~

This script counts eojeol

Yejin Cho (scarletcho@gmail.com)

Last updated: 2016-12-13
"""

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

in_fname = 'sejong_normalized_v2.0.txt'
# in_fname = 'sejong_beforenormal.txt'

corpus = open(in_fname, 'r')
cnt = 0
for line in corpus:
    cnt += len(re.findall(u'\s', line))

print cnt