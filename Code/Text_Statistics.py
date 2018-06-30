
"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

import os
import re
import jieba
import jieba.posseg as pseg
import jieba.analyse


seg_list_file_addr = os.listdir('D:\DataMiningCourse\加贺恭一郎系列')
print(seg_list_file_addr)


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords


def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('D:\DataMiningCourse\\停用词.txt')
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += ""
    return outstr


# 统计主动句、被动句、疑问句和反问句；
# 按句划分，保存主谓宾结构
Quest_cnt = 0
State_cnt = 0
Reverse_Quest_cnt = 0
Active_cnt = 0
Passive_cnt = 0
text_list = open('D:\DataMiningCourse\神探伽利略系列\\伽利略的苦恼02 操纵.txt', 'r',encoding='gbk')
text_list2 = open('D:\DataMiningCourse\\伽利略小说人物(1).txt', 'r', encoding='UTF-8')
sentence_output = open('D:\DataMiningCourse\神探伽利略系列\\sentence_output.txt', 'w', encoding='UTF-8', errors='ignore')

jieba.load_userdict(text_list2)
temp_character = []
dict_character_verb = {}
dict_freq = {}

for line in text_list.readlines():
    if '？' in line:
        Quest_cnt += 1
    else:
        State_cnt += 1
    if ('难道' in line and '？' in line) or ('怎能' in line and '？' in line) or ('怎么' in line and '能' in line) or ('怎么' in line and '就' in line) or ('不' in line and '？' in line) or ('没有' in line and '？' in line):
        Reverse_Quest_cnt += 1
    else:
        Active_cnt += 1
    if '被' in line or ('受' in line and '所' in line)or ('为' in line and '所' in line):
        Passive_cnt += 1

    split_list = re.split(r'[。？！]', line)
    for sentence in split_list:
        temp_character.clear()
        temp_action = ''
        seg_list = jieba.cut(sentence, cut_all=True)
        sentence_seg = seg_sentence(sentence)
        words = pseg.cut(sentence_seg)
        for word in words:
            sentence_output.write(word.word + '(' + word.flag + ')')
            if word.flag == "nr":
                temp_character.append(word.word)
            if word.flag == 'v':
                temp_action = word.word
            if word.word in dict_freq:
                dict_freq[word.word] += 1
            else:
                dict_freq[word.word] = 1
        if len(temp_character) > 1 and temp_action != '':
            dict_character_verb[temp_action] = temp_character[0] + temp_action + temp_character[1]
        sentence_output.write('\n')

print(dict_character_verb)
sentence_output.write(str(Quest_cnt) + '\n')
sentence_output.write(str(Reverse_Quest_cnt) + '\n')
sentence_output.write(str(Passive_cnt) + '\n')
print(Quest_cnt)
print(State_cnt)
print(Reverse_Quest_cnt)
print(Passive_cnt)
print(Active_cnt)
