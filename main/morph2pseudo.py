# -*- coding: utf-8 -*-
"""
morph2pseudo.py
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
        hanja  ($ pip install hanja)

Yejin Cho (scarletcho@gmail.com)

Last updated: 2016-12-22
"""

import re
import sys
from konlpy.utils import pprint
from hanja import hangul

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


def writefile(body, fname):
    out = open(fname, 'w')
    for line in body:
        out.write('{}\n'.format(line))
    out.close()


def getStrIndices(myiter, mystring):
    idxlist = []
    for m in myiter:
        startIndex = m.start()
        endIndex = m.end()
        idxlist.append([m.span(), mystring[startIndex:endIndex]])
    return idxlist


def getEojeolList(sentlist):
    output_stack = []

    for sent_id in range(0, len(sentlist)):
        sent = sentlist[sent_id]
        eojeol_list = sent.split(' ')
        output_stack.append(eojeol_list)

    return output_stack


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
                        idx = idx + 1   # Keep investigating
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

                    else:   # Endpoint reached
                        # print('END!')
                        end_idx = idx
                        end_unreached = False
                        break


                else:   # No NOUN matched
                    # print('NO MATCH!')
                    seq = seq + idxlist_morph[idx][1]

                    if idx < len(idxlist_pos) - 1:   # Endpoint not reached yet
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
    # print('pseudo-simple: ')
    # pprint(out_simple)
    # print('\n')
    return out_simple


def morph2pseudo(raw_sentlist, morph_sentlist, type):
    # Data type conversion in case the input is given as string
    if isinstance(raw_sentlist, basestring):
        raw_sentlist = [raw_sentlist]
    if isinstance(morph_sentlist, basestring):
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
            morph_eojeol_sentlist = sent.split(' ')
            pseudo_intermediate.append(morph_eojeol_sentlist)

        eojeol_sentlist = getEojeolList(raw_sentlist)


        # For each sentence in input list
        out_classic = []
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

            out_classic.append(pseudo_sent)

        out_classic = tightenString(out_classic)

        # print('pseudo-classic: ')
        # pprint(out_classic)
        # print('\n')
        return out_classic



# # ------------------------------------------------------------------------------------------------
# # [1] Input by giving a SINGLE variable in script

# raw = [u'에프 일 이선과의 인연을 이루지 못하고 옥에서 죽게 되었다']
        # [u'공모한않았다면'] # [u'새우볶음밥이 좋아요']
# morph = [u'에프__05/NNG 일__05/NR 이__09/NR+선__14/NNG+과/JKB+의/JKG 인연__03/NNG+을/JKO 이루__01/VV+지/EC 못하/VX+고/EC 옥__04/NNG+에서/JKB 죽__01/VV+게/EC 되__01/VV+었/EP+다/EC+돐__01/NNG+?/SW+_/SW+10/SN+//SP+?SL+쮊/NNG+/SW+/SW']
        # [u'공모하__01/VV+ㄴ/ETM+않/VX+았/EP+다면/EC']
# [u'새우볶음/NNG+밥__05/NNG+이/JKS 좋__08/VA+아요/EF']
#
# out_classic = morph2pseudo(raw, morph, 'classic')
# pprint(out_classic)
# out_simple = morph2pseudo(raw, morph, 'simple')
# pprint(out_simple)

# # ------------------------------------------------------------------------------------------------
# # [2] Input by variables in script
#
# raw_sentlist = [u'칠반아이가 몸이 불편한 줄 알고 있으면서 괴롭힙니다',
#                 u'다시 이성을 찾은 음성으로 다희가 짧게 말했다',
#                 u'그 돈은 효철이 다희의 입원비로 대신 물어준 백만 원이었다',
#                 u'빳빳한 종잇장 얇디얇은 수표 한 장이 효철의 가슴을 칼날처럼 그으며 지나가는 것 같았다',
#                 u'칼날이 지나간 자리마다 선홍색 피가 스며나왔고 효철은 저도 모르게 속으로 아아아 비명을 질렀다',
#                 u'그리고 싸늘한 바람이 영혼까지 쪼개며 지나가는 것 같아 효철은 한순간 정신이 아득해졌다']
#
# morph_sentlist = [
#     u'칠__02/NNG+반__07/NNG+아이__01/NNG+가/JKS 몸__01/NNG+이/JKS 불편하__01/VA+ㄴ/ETM 줄__04/NNB 알/VV+고/EC 있__01/VX+으면서/EC 괴롭히/VV+ㅂ니다/EF',
#     u'다시__01/MAG 이성__08/NNG+을/JKO 찾/VV+은/ETM 음성__02/NNG+으로/JKB 다희/NNP+가/JKS 짧/VA+게/EC 말하/VV+였/EP+다/EC',
#     u'그__01/MM 돈__01/NNG+은/JX 효철/NNP+이/JKS 다희/NNP+의/JKG 입원비/NNG+로/JKB 대신__03/NNG 물__03/VV+어/EC+주__01/VX+ㄴ/ETM 백만/NR 원__01/NNB+이/VCP+었/EP+다/EC',
#     u'빳빳하/VA+ㄴ/ETM 종잇장/NNG 얇디얇/VA+은/ETM 수표__01/NNG 한__01/MM 장__22/NNB+이/JKS 효철/NNP+의/JKG 가슴__01/NNG+을/JKO 칼날/NNG+처럼/JKB 긋__01/VV+으며/EC 지나가/VV+는/ETM 것__01/NNB 같/VA+았/EP+다/EC',
#     u'칼날/NNG+이/JKS 지나가/VV+ㄴ/ETM 자리__01/NNG+마다/JX 선홍색/NNG 피__02/NNG+가/JKS 스미/VV+어/EC+나오/VV+았/EP+고/EC 효철/NNP+은/JX 저__03/NP+도/JX 모르/VV+게/EC 속__01/NNG+으로/JKB 아아아/IC 비명__02/NNG+을/JKO 지르__03/VV+었/EP+다/EC',
#     u'그리고/MAJ 싸늘하/VA+ㄴ/ETM 바람__01/NNG+이/JKS 영혼__02/NNG+까지/JX 쪼개/VV+며/EC 지나가/VV+는/ETM 것__01/NNB 같/VA+아/EC 효철/NNP+은/JX 한순간/NNG 정신__12/NNG+이/JKS 아득하/VA+여/EC+지__04/VX+었/EP+다/EF']
#
# output_classic = morph2pseudo(raw_sentlist, morph_sentlist, 'classic')
# output_simple = morph2pseudo(raw_sentlist, morph_sentlist, 'simple')
#
# # ------------------------------------------------------------------------------------------------
# # [3] Input by file

# *** CHANGE PATH ACCORDING TO YOUR ENVIRONMENT:
rawText = '/Users/Scarlet_Mac/Downloads/textraw_readspeech.txt'
morphText = '/Users/Scarlet_Mac/Downloads/textraw_readspeech.txt.tag'

# or simply:
# rawText = 'sampleRaw.txt'
# morphText = 'sampleMorph.txt'

print('(1) READ FILE IN UTF8 ENCODING')
corpus = tightenString(readfileUTF8(rawText))
morph = tightenString(readfileUTF8(morphText))

print('(2) MORPH -> PSEUDO: simple')
output_simple = morph2pseudo(corpus, morph, 'simple')

print('(3) WRITE OUTPUT: simple')
writefile(output_simple, 'readpseudo_simple.txt')


print('(2) MORPH -> PSEUDO: classic')
output_classic = morph2pseudo(corpus, morph, 'classic')

print('(3) WRITE OUTPUT: classic')
writefile(output_classic, 'readpseudo_classic.txt')


# # ------------------------------------------------------------------------------------------------