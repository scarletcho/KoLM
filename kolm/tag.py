# -*- coding: utf-8 -*-
"""
tag.py
~~~~~~~~~~

This script converts morpheme tagged text into pseudo-morphemes.

Input: 1) List of raw text (unicode)
       2) List of morpheme-analyzed text (unicode)
       3) Type of pseudo-morpheme:
            - 'classic':  conventional style
            - 'simple':   simplified style which only separates noun clusters out

Output: A text file (or list variable) with pseudo-morpheme boundaries.

Usage: morph2pseudo([u'raw_string'], [u'morphed_string'], classic_or_simple)


[NOTE] Please download the required python packages via pip command:
        KoNLPy ($ pip install JPype1
                $ pip install konlpy)
        Mecab  ($ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh))
        hanja  ($ pip install hanja)

Yejin Cho (scarletcho@gmail.com)

Last updated: 2017-02-22
"""

import sys
import re
from hanja import hangul
from konlpy.tag import Mecab
from kolm.utils import *

# Check Python version
ver_info = sys.version_info

if ver_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


def morphTag(in_fname, out_fname):
    mec = Mecab()
    corpus = readfileUTF8(in_fname)
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
    writefile(concat_sent, out_fname)

    return concat_sent


def getStrIndices(myiter, mystring):
    idxlist = []
    for m in myiter:
        startIndex = m.start()
        endIndex = m.end()
        idxlist.append([m.span(), mystring[startIndex:endIndex]])
    return idxlist


def concatNouns(eojeol_list):
    try:
        output = []

        for eoj_id in range(0, len(eojeol_list)):
            eoj = eojeol_list[eoj_id]

            morph = re.finditer(u'[ㄱ-힣]+', eoj)
            pos = re.finditer(u'[A-Z]+', eoj)

            idxlist_morph = getStrIndices(morph, eoj)
            idxlist_pos = getStrIndices(pos, eoj)

            idx = 0
            seq = ''
            end_unreached = True
            noun = re.compile(u'(NNG|NNP|NNB|NR|NP|XPN|XSN)')

            while end_unreached:

                # Beginning of NOUN sequence
                if re.match(noun, idxlist_pos[idx][1]):
                    # print(idxlist_pos[idx][1] + '==> INIT')
                    seq = seq + idxlist_morph[idx][1]
                    init_idx = idx

                    if idx < len(idxlist_pos) - 1:  # Endpoint not reached yet
                        idx = idx + 1  # Keep investigating
                        continuity = True

                        while continuity:
                            if re.match(noun, idxlist_pos[idx][1]):
                                # NOUN sequence continues
                                # print(idxlist_pos[idx][1] + '==> CONTINUE')
                                seq = seq + idxlist_morph[idx][1]

                                if idx < len(idxlist_pos) - 1:  # Endpoint not reached yet
                                    idx = idx + 1  # Keep investigating

                                else:  # Endpoint reached
                                    continuity = False
                                    end_unreached = False

                            else:  # NOUN sequence ends
                                continuity = False
                                # print('END!')
                                seq = seq + u'+' + idxlist_morph[idx][1]
                                end_idx = idx - 1

                                if idx < len(idxlist_pos) - 1:  # Endpoint not reached yet
                                    idx = idx + 1  # Keep investigating

                                else:  # Endpoint reached
                                    continuity = False
                                    end_unreached = False

                    else:  # Endpoint reached
                        # print('END!')
                        end_idx = idx
                        end_unreached = False
                        break


                else:  # No NOUN matched
                    # print('NO MATCH!')
                    seq = seq + idxlist_morph[idx][1]

                    if idx < len(idxlist_pos) - 1:  # Endpoint not reached yet
                        idx = idx + 1  # Keep investigating

                    else:  # Endpoint reached
                        end_unreached = False
                        init_idx = ''
                        end_idx = ''

            output.append(seq)
    except:
        output = False
    return output


def sameCheck(input_string1, input_string2):
    # 유니코드 한글을 비교하여 유사도 리턴.
    # 0 - 초,중,종 모두 다름
    # 1 - 한개가 같음
    # 2 - 두개가 같음
    # 3 - 동일한 글자

    # 단일 자음은 종성으로 간주하고 convert_dictionary 를 이용하여 유사도 비교
    convert_dictionary = {1: 5, 4: 8, 7: 11, 8: 13, 16: 21, 17: 22, 19: 25,
                          21: 27, 22: 0, 23: 2, 24: 3, 25: 4, 26: 5, 27: 6, 0: 0}

    var1 = hangul.separate(input_string1)
    var2 = hangul.separate(input_string2)

    same_point = 0

    if var1[0] == -75:  # 한글이 아닌 기호여서, full match 만 해야 함
        for index in range(0, 3):
            if var1[index] == var2[index]:
                if index == 2:
                    if var1[index] != 0:
                        same_point += 1
                else:
                    same_point += 1
        if same_point == 3:
            return 3
        else:
            return 0
    else:
        if var2[0] == -54 and var2[1] == 11:  # 단독자음 처리
            if convert_dictionary[var1[2]] == var2[2]:
                return 1

        for index in range(0, 3):  # 한글 처리
            if var1[index] == var2[index]:
                if index == 2:
                    if var1[index] != 0:
                        same_point += 1
                else:
                    same_point += 1

    return same_point


def pseudoClassic(raw, morphed):
    result_buffer = []
    carry_buffer = []

    index_i = 0
    index_j = 0

    try:
        is_loop = True

        while is_loop:
            same_check_value = sameCheck(raw[index_i], morphed[index_j])  # 유사도 계산 (0~3)

            if same_check_value >= 2:  # 유사도 2 이상이므로 결과에 포함
                if raw[index_i] != u"'":  # '가 아닌 경우에만 플러스 처리를 한다. 약간 ad-hoc
                    if len(carry_buffer) > 0:  # carry 에 데이터가 남아있고, +를 포함하고 있으면
                        if u'+' in carry_buffer:
                            result_buffer.append(u'+')
                        carry_buffer = []
                result_buffer.append(raw[index_i])
                index_i += 1
                index_j += 1

            elif same_check_value == 1:  # 유사도 1을 검출함

                is_second_loop = True

                while is_second_loop:
                    if len(morphed) - 1 >= index_j:  # 두번째 데이타가 남아있으면 다음 데이타를 확인함
                        second_same_check_value = sameCheck(raw[index_i], morphed[index_j])

                        if second_same_check_value >= 1:  # 나머지 유사도 1을 찾음
                            if len(carry_buffer) > 0:  # carry 에 데이타가 남아있고, +를 포함하고 있으면
                                if u'+' in carry_buffer:
                                    result_buffer.append(u'+')
                                carry_buffer = []
                            result_buffer.append(raw[index_i])
                            index_i += 1
                            is_second_loop = False
                        index_j += 1

                    else:  # 남아있지 않으면 루프 중단
                        is_second_loop = False

            else:  # 유사도가 없음
                carry_buffer.append(morphed[index_j])
                index_j += 1

            if index_i >= len(raw):  # 종료 확인
                is_loop = False

            if index_j >= len(morphed):  # 종료 확인
                if len(carry_buffer) > 0:
                    if u'+' in carry_buffer:
                        result_buffer.append(u'+')
                    result_buffer.append(raw[index_i])
                is_loop = False
    except:
        result_buffer = raw

    return ''.join(result_buffer)


def pseudoSimple(raw_sentlist, morph_sentlist):
    eojeol_sentlist = getEojeolList(raw_sentlist)

    pseudo_intermediate = []
    for sent_id in range(0, len(morph_sentlist)):
        print('sentence #: ' + str(sent_id))
        sent = re.sub(u'[_/\d]', '', morph_sentlist[sent_id])
        morph_eojeol_sentlist = sent.split(' ')

        output = concatNouns(morph_eojeol_sentlist)
        if not output:
            output = eojeol_sentlist[sent_id]
        pseudo_intermediate.append(output)

    # For each sentence in input list
    out_simple = []
    for sentIdx in range(0, len(eojeol_sentlist)):
        print('sentence #: ' + str(sentIdx))
        eoj = eojeol_sentlist[sentIdx]
        pseu = pseudo_intermediate[sentIdx]

        # For each item in input sentence(s)
        pseudo_sent = ''
        for itemIdx in range(0, len(eoj)):
            e = eoj[itemIdx]
            p = pseu[itemIdx]

            pseudo_item = pseudoClassic(e, p)
            pseudo_sent = pseudo_sent + ' ' + pseudo_item

        out_simple.append(pseudo_sent)

    out_simple = tightenString(out_simple)
    return out_simple


def morph2pseudo(raw_sentlist, morph_sentlist, type):
    # Data type conversion in case the input is given as string
    if isinstance(raw_sentlist, str):
        raw_sentlist = [raw_sentlist]
    if isinstance(morph_sentlist, str):
        morph_sentlist = [morph_sentlist]

    # (1) Convert to SIMPLE pseudo-morpheme
    if type == 'simple':
        out_simple = pseudoSimple(raw_sentlist, morph_sentlist)
        return out_simple

    # (2) Convert to CLASSIC pseudo-morpheme
    elif type == 'classic':
        pseudo_intermediate = []
        for sent_id in range(0, len(morph_sentlist)):
            sent = re.sub(u'[_/\dA-Z]', '', morph_sentlist[sent_id])
            morph_eojeol_sentlist = sent.split(u' ')
            pseudo_intermediate.append(morph_eojeol_sentlist)

        eojeol_sentlist = getEojeolList(raw_sentlist)

        # For each sentence in input list
        out_classic = []
        for sentIdx in range(0, len(eojeol_sentlist)):
            print('sentence #: ' + str(sentIdx))
            eoj = eojeol_sentlist[sentIdx]
            pseu = pseudo_intermediate[sentIdx]

            # For each item in input sentence(s)
            pseudo_sent = u''
            for itemIdx in range(0, len(eoj)):
                e = eoj[itemIdx]
                p = pseu[itemIdx]

                pseudo_item = pseudoClassic(e, p)
                pseudo_sent = pseudo_sent + u' ' + pseudo_item

            out_classic.append(pseudo_sent)

        out_classic = tightenString(out_classic)

        return out_classic


def pseudomorph(rawText, morphText, pseudoType):
    print('(1) READ FILE IN UTF8 ENCODING')
    corpus = readfileUTF8(rawText)
    morph = readfileUTF8(morphText)

    if pseudoType == 'simple':
        print('(2) MORPH -> PSEUDO: simple')
        output_simple = morph2pseudo(corpus, morph, 'simple')

        print('(3) WRITE OUTPUT: simple')
        writefile(output_simple, 'simple.txt')
        print('Process finished')

    elif pseudoType == 'classic':
        print('(2) MORPH -> PSEUDO: classic')
        output_classic = morph2pseudo(corpus, morph, 'classic')

        print('(3) WRITE OUTPUT: classic')
        writefile(output_classic, 'classic.txt')
        print('Process finished')

