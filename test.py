# -*- coding: utf-8 -*-

import sys
import re
from hanja import hangul
from konlpy.tag import Mecab
from . import utils

reload(sys)
sys.setdefaultencoding('utf-8')


# def morphTag(in_fname, out_fname):
mec = Mecab()
corpus = utils.readfileUTF8(in_fname)
concat_sent = []
for n in range(0, len(corpus)):
    tagged = mec.pos(corpus[n])
    concat = ''
    for m in range(0, len(tagged)):
        if m < len(tagged):
            concat = concat + tagged[m][0] + '/' + tagged[m][1] + ' '
        elif m == len(tagged):  # When reached the final item
            concat = concat + tagged[m][0] + '/' + tagged[m][1]

    concat_sent.append(concat)
utils.writefile(concat_sent, out_fname)

    # return concat_sent
