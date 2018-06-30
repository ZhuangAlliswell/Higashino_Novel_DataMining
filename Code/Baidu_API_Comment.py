
"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

from aip import AipNlp
import os
import re
import jieba
import jieba.analyse
import jieba.posseg as pseg
import csv

addr = 'D:\DataMiningCourse\知乎问题分类'
file_type_addr = os.listdir(addr)
print(file_type_addr)

motion_analyse_output_addr = 'D:\DataMiningCourse\知乎问题分类\\'
# motion_analyse_output = open('D:\DataMiningCourse\加贺系列输出\\motion_analyse.txt', 'w', encoding='utf-8', errors='ignore')

# 定义常量
APP_ID = '10582984'
API_KEY = 'ZSifoOGYo7O8cf4FUkRNrxuL'
SECRET_KEY = 'BpjTGC2mPKxouiIKtprxsuEsrypcv4tj '
# 初始化AipNlp对象
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
posi, nega  = [] ,[]


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


# sub file
for file in file_type_addr:
    print('file: ' + file)
    comment_file = addr + '\\' + file
    file_addr = os.listdir(comment_file)
    print('file_addr: ' + str(file_addr))
    csvFile = open(motion_analyse_output_addr + file + '_comment_analyse.txt.csv', 'w', newline='')  # 设置newline，否则两行之间会空一行
    for txt_file in file_addr:

        text_list = open(addr + '\\' + file + '\\' + txt_file, 'r', encoding='gbk')

        dict_comment_freq = {}

        for line in text_list.readlines():
            if line != '====================':
                split_list = re.split(r'[。？！]', line)
                for sentence in split_list:
                    temp_action = ''
                    seg_list = jieba.cut(sentence, cut_all=True)
                    sentence_seg = seg_sentence(sentence)
                    words = pseg.cut(sentence_seg)
                    for word in words:
                        if word.flag == "n" or word.flag == 'v' or word.flag == 'a':
                            if word.word in dict_comment_freq:
                                dict_comment_freq[word.word] += 1
                            else:
                                dict_comment_freq[word.word] = 1

    dict_freq_sorted = sorted(dict_comment_freq.items(), key=lambda item: item[1], reverse=True)
    writer = csv.writer(csvFile)
    for i in range(len(dict_freq_sorted)):
        writer.writerow(dict_freq_sorted[i])
    csvFile.close()


