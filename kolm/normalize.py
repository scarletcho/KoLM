# -*- coding: utf-8 -*-
"""
normalize.py
~~~~~~~~~~

This script conducts text normalization on Korean corpora.
Details are designed for normalizing Sejong 21st written corpus.


[NOTE] Please download the required python packages via pip command:
        korean ($ pip install korean)
        hanja  ($ pip install hanja)

Yejin Cho (scarletcho@gmail.com)
Yeonjung Hong (yvonne.yj.hong@gmail.com)

Last updated: 2017-02-22
"""

import re
import sys
import datetime as dt
import hanja
from korean import NumberWord, Loanword
from . import utils


# Check Python version
ver_info = sys.version_info

if ver_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


def bySentence(corpus):
    import re
    body = []  # init body
    for line in corpus:
        # Map '…' into '.'
        line = re.sub('…', u'.', line)
        # [Note] Do NOT put 'u' before '…'. Unicode doesn't work in this case.

        # Delete periods included in initial letter sequences
        line = re.sub(u'(?<=\.[A-Z])\.', u'', line)
        line = re.sub(u'(?<=[A-Z])\.(?=[A-Z])', u'', line)

        # Clean up multiple punctuations (ex: 'Hi!!!' -> 'Hi!')
        line = re.sub(u'\.+', u'.', line)
        line = re.sub(u'\?+', u'?', line)
        line = re.sub(u'\!+', u'!', line)

        # Split by sentence final punctuation marks
        # (i.e. period '.', question mark '?', exclamation mark '!')
        line = re.sub(u'(?<=[\.\?\!])[ \,]', u'\n', line)  # Space/comma after punctuations '.', '!', '?'
        line = re.sub(u'(?<=[가-힣])[\.\?\!](?=[가-힣])', u'.\n', line)  # Punctuations with no space afterwards
        line = line.splitlines()

        for shorterline in line:
            if not shorterline.isspace():  # Space check
                if shorterline:  # Emptiness check
                    if sys.version_info[0] == 2:
                        body.append(unicode(shorterline))
                    else:
                        body.append(shorterline)

    return body


def normalize(corpus):
    body = []  # init body
    for line in corpus:
        # Number deletion
        line = re.sub(u'^\s*[\(\[<〈《【〔]*\s*\d+[\)\.\]>〉》】〕](?=\D+)', u'', line)

        # Number reading
        line = readNumber(line)

        # Deletion
        line = re.sub(u'(\(예:.*?\)|\[예:.*?\]|^[ \t]*예:.*?)', u'', line)  # examples
        line = re.sub(u'^\s*[\(\[<〈《【〔]*\s*[ㄱ-ㅎ가-힣][\)\]>〉》】〕]\s*(?=[가-힣]*)', u'', line)  # ordered bullets
        line = re.sub(u'\([^\)]*[^\)]+\)', u'', line)  # Everything within parentheses '()'
        line = re.sub(
            u'(file://|gopher://|news://|nntp://|telnet://|https?://|ftps?://|sftp://|www\.)([a-z0-9-]+\.)+[a-z0-9]{2,4}[^ㄱ-힣\)\]\.\,\'\"\s]*''',
            u'', line)  # web address
        line = re.sub(u'[ㅡ-]*', u'', line)  # dashes
        line = re.sub(u'[\`\'\"＂‘’“”]*', u'', line)  # quotations
        line = re.sub(u'【.*?기자[ \t]*】', u'', line)  # reporter's name
        line = re.sub(u'〔.*?〕', u'', line)  # book's title as reference
        line = re.sub(u'[\[〈〉《》「」『』{}\]]*', u'', line)  # brackets
        line = re.sub(u'(\w+[\w\.]*)@(\w+[\w\.]*)\.([A-Za-z]+)', u'', line)  # email address
        line = re.sub(u'\#', u'', line)  # sharp
        line = re.sub(u'(?<=[가-힣])[A-Za-z]+[ ]?[A-Za-z]*', u'', line)  # alphabet references right after hangul

        # Substitution into newline
        line = re.sub(u'[=:;]', u'\n', line)  # colon ':' or semi-colon ';'

        # Substitution into whitespace
        line = re.sub(u'·', u' ', line)  # '·'
        line = re.sub(u'(?<=[가-힣A-Za-z])~(?=[가-힣A-Za-z]+)', u' ', line)  # tide '~' between words
        line = re.sub(u'→', u' ', line)  # arrow '→'

        # Hangul jaum (single consonants) reading
        line = readHangulLetter(line)

        # Hanja (Chinese character) reading
        line = readHanja(line)

        # ABC (capital letter sequences) reading
        line = readABC(line)

        # Alphabet reading
        line = readAlphabet(line, 'ita')

        # Remove all non-hangul characters
        line = removeNonHangul(line)

        if not line.isspace():  # Space check
            if line:  # Emptiness check
                if sys.version_info[0] == 2:
                    body.append(unicode(line))
                else:
                    body.append(line)

    return body


def readNumber(line):
    numlist = []

    for numiter in re.finditer(u'([+-]?\d+)[\.]?\d*', line):
        numlist.append(numiter.group())

    if len(numlist) > 0:
        for i in range(0, len(numlist)):
            # Re-initialize numidx & numlist stack
            numidx = []
            numlist = []

            for numiter_fresh in re.finditer(u'([+-]?\d+)[\.]?\d*', line):
                numidx.append(numiter_fresh.span())
                numlist.append(numiter_fresh.group())

            while len(numlist) > 0:
                num = numlist[0]
                break

            if re.search('\.', num) is None:
                # [Case 1] Integer
                numint = re.search(u'\d+', num).group()
                numint = NumberWord(int(numint)).read()
                num = re.sub(u'\d+', numint, num)

            else:  # [Case 2] Floating number
                # Read integer part first
                numint = re.search(u'\d+(?=\.)', num).group()
                numint = NumberWord(int(numint)).read()
                num = re.sub(u'\d+(?=\.)', numint, num)

                # Read floating points
                num = re.sub(u'\.', u'점', num)
                num = re.sub(u'0', u'영', num)
                num = re.sub(u'1', u'일', num)
                num = re.sub(u'2', u'이', num)
                num = re.sub(u'3', u'삼', num)
                num = re.sub(u'4', u'사', num)
                num = re.sub(u'5', u'오', num)
                num = re.sub(u'6', u'육', num)
                num = re.sub(u'7', u'칠', num)
                num = re.sub(u'8', u'팔', num)
                num = re.sub(u'9', u'구', num)

            ituple = numidx[0]
            numlist[0] = num

            line = replaceSubstring(line, num, ituple)
    return line


def readHanja(line):
    if re.search(u'[一-龥豈-龎]+', line):
        if re.search(u'[가-힣]+[一-龥豈-龎]+', line):
            line = re.sub(u'[一-龥豈-龎]+', u'', line)
        else:
            line = hanja.translate(line, 'substitution')
    return line


def readABC(line):
    ABClist = []

    for ABCiter in re.finditer(u'[A-Z](?=[^a-z])', line):
        ABClist.append(ABCiter.group())

    if len(ABClist) > 0:
        for i in range(0, len(ABClist)):
            # Re-initialize alphaidx & alphalist stack
            ABCidx = []
            ABClist = []

            for ABCiter_fresh in re.finditer(u'[A-Z](?=[^a-z])', line):
                ABCidx.append(ABCiter_fresh.span())
                ABClist.append(ABCiter_fresh.group())

            while len(ABClist) > 0:
                ABC = ABClist[0]
                break

            ABC = re.sub(u'A', u'에이', ABC)
            ABC = re.sub(u'B', u'비', ABC)
            ABC = re.sub(u'C', u'씨', ABC)
            ABC = re.sub(u'D', u'디', ABC)
            ABC = re.sub(u'E', u'이', ABC)
            ABC = re.sub(u'F', u'에프', ABC)
            ABC = re.sub(u'G', u'지', ABC)
            ABC = re.sub(u'H', u'에이치', ABC)
            ABC = re.sub(u'I', u'아이', ABC)
            ABC = re.sub(u'J', u'제이', ABC)
            ABC = re.sub(u'K', u'케이', ABC)
            ABC = re.sub(u'L', u'엘', ABC)
            ABC = re.sub(u'M', u'엠', ABC)
            ABC = re.sub(u'N', u'엔', ABC)
            ABC = re.sub(u'O', u'오', ABC)
            ABC = re.sub(u'P', u'피', ABC)
            ABC = re.sub(u'Q', u'큐', ABC)
            ABC = re.sub(u'R', u'알', ABC)
            ABC = re.sub(u'S', u'에스', ABC)
            ABC = re.sub(u'T', u'티', ABC)
            ABC = re.sub(u'U', u'유', ABC)
            ABC = re.sub(u'V', u'브이', ABC)
            ABC = re.sub(u'W', u'더블유', ABC)
            ABC = re.sub(u'X', u'엑스', ABC)
            ABC = re.sub(u'Y', u'와이', ABC)
            ABC = re.sub(u'Z', u'지', ABC)

            ituple = ABCidx[0]
            ABClist[0] = ABC

            line = replaceSubstring(line, ABC, ituple)

    return line


def readAlphabet(line, lang):
    alphalist = []

    for alphaiter in re.finditer(u'[A-Za-z]+', line):
        alphalist.append(alphaiter.group())

    if len(alphalist) > 0:
        for i in range(0, len(alphalist)):
            # Re-initialize alphaidx & alphalist stack
            alphaidx = []
            alphalist = []

            for alphaiter_fresh in re.finditer(u'[A-Za-z]+', line):
                alphaidx.append(alphaiter_fresh.span())
                alphalist.append(alphaiter_fresh.group())

            while len(alphalist) > 0:
                alpha = alphalist[0]
                break

            alpha = Loanword(alpha, lang).read()

            ituple = alphaidx[0]
            alphalist[0] = alpha

            line = replaceSubstring(line, alpha, ituple)
    return line


def replaceSubstring(line, newstr, ituple):
    output = line[0:ituple[0]] + newstr + line[ituple[1]:]
    return output


def removeNonHangul(line):
    line = re.sub(u'[^가-힣\s]*', u'', line)
    return line


def readHangulLetter(line):
    line = re.sub(u'ㄱ', u'기역', line)
    line = re.sub(u'ㄴ', u'니은', line)
    line = re.sub(u'ㄷ', u'디귿', line)
    line = re.sub(u'ㄹ', u'리을', line)
    line = re.sub(u'ㅁ', u'미음', line)
    line = re.sub(u'ㅂ', u'비읍', line)
    line = re.sub(u'ㅅ', u'시옷', line)
    line = re.sub(u'ㅇ', u'이응', line)
    line = re.sub(u'ㅈ', u'지읒', line)
    line = re.sub(u'ㅊ', u'치읓', line)
    line = re.sub(u'ㅎ', u'히읗', line)

    line = re.sub(u'ㄲ', u'쌍기역', line)
    line = re.sub(u'ㄸ', u'쌍디귿', line)
    line = re.sub(u'ㅃ', u'쌍비읍', line)
    line = re.sub(u'ㅆ', u'쌍시옷', line)
    line = re.sub(u'ㅉ', u'쌍지읒', line)
    return line


def Knormalize(in_fname, out_fname):
    # Mark beginning time
    beg = dt.datetime.now()
    corpus = open(in_fname, 'r')

    # Re-arrange corpus by sentence based on punctuations
    body = bySentence(corpus)
    total_count_original = len(body)
    print("[Step 1] Splitted by sentence")

    # Tighten string by deleting surrounding spaces
    body = utils.tightenString(body)
    print("[Step 2] Text tightened removing extra spaces")

    # Re-arrange corpus by sentence based on punctuations
    body = bySentence(body)
    print("[Step 3] Re-Splitted by sentence")

    # Normalize text in general & Remove everything except hangul
    body = normalize(body)
    print("[Step 4] Normalization completed")

    # Re-arrange body by sentence based on punctuations
    body = bySentence(body)
    print("[Step 5] Re-splitted by sentence")

    # Final tightening up: Remove all surrounding whitespaces
    body = utils.tightenString(body)
    print("[Step 6] Final text tightening done")
    # pprint(body)


    end = dt.datetime.now()
    print(end - beg)

    print("Original text length by line number: " + str(total_count_original))
    print("Normalized text length by line number: " + str(len(body)))

    utils.writefile(body, out_fname)

