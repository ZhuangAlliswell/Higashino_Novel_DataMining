
"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

import jieba
import os
import jieba.posseg as pseg
import jieba.analyse
# from collection import Counter


seg_list_file_addr = os.listdir('D:\DataMiningCourse\加贺恭一郎系列')
print(seg_list_file_addr)

dict_character_verb = {}
temp_character = []
dict_freq = {}


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
                outstr += " "
    return outstr


# Raw text file
text_list1 = open('D:\DataMiningCourse\加贺恭一郎系列\\毕业前杀人游戏.txt', 'r')
text_list2 = open('D:\DataMiningCourse\\jpname.txt', 'r', encoding = 'UTF-8')
# Output file
outputs = open('D:\DataMiningCourse\加贺恭一郎系列\\output.txt', 'w')
seg_output = open('D:\DataMiningCourse\加贺恭一郎系列\\seg_output.txt', 'w')
words_flag = open('D:\DataMiningCourse\加贺恭一郎系列\\words_flag.txt', 'w')


jieba.load_userdict(text_list2)
raw_text = text_list1.read()

line_seg = seg_sentence(raw_text)
outputs.write(line_seg + '\n')
outputs.close()

seg_list = jieba.cut(raw_text, cut_all=True)
print("Full Mode: " + " ".join(seg_list))
seg_output.write("Full Mode: " + " ".join(seg_list))

seg_list = jieba.cut(raw_text, cut_all=False)
print("Default Mode: " + " ".join(seg_list))
seg_output.write("Default Mode: " + " ".join(seg_list))

text_list3 = open('D:\DataMiningCourse\加贺恭一郎系列\\output.txt', 'r')

for line in text_list3.readlines():
    line = line.strip()
    temp_character.clear()
    temp_action = ''
    # Place、Noun、Ver、Adj、Adv
    keywords = jieba.analyse.textrank(line, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'a', 'ad'))
    for item in keywords:
        words_flag.write(str(item[0]) + ' ' + str(item[1]) + ' ')
    words = pseg.cut(line)
    for word in words:
        words_flag.write(word.word + word.flag)
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
    words_flag.write('\n')

keywords = jieba.analyse.textrank(raw_text, topK=100, withWeight=True, allowPOS=('a', 'ad'))
for item in keywords:
    words_flag.write(item[0] + ' ' + str(item[1]) + '\n')

keywords = jieba.analyse.textrank(raw_text, topK=100, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
for item in keywords:
    words_flag.write(item[0] + ' ' + str(item[1]) + '\n')

words_flag.close()
print(dict_character_verb)
print(dict_freq)



