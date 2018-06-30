
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

motion_analyse_output_addr = 'D:\DataMiningCourse\知乎问题分类处理\\'

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

    for txt_file in file_addr:
        Comment_key = open(motion_analyse_output_addr + file + '\\' + txt_file + '_comment_key.txt', 'w', encoding='UTF-8', errors='ignore')  # 设置newline，否则两行之间会空一行
        text_list = open(addr + '\\' + file + '\\' + txt_file, 'r', encoding='gbk')
        raw_text = text_list.read()
        Comment_key.write('Position: ' + '\n')
        keywords = jieba.analyse.textrank(raw_text, topK=10, withWeight=True, allowPOS=('ns'))
        for item in keywords:
            Comment_key.write(item[0] + ': ' + str(item[1]) + '\n')
            Comment_key.write('\n')
        Comment_key.write('Verb: ' + '\n')
        keywords = jieba.analyse.textrank(raw_text, topK=10, withWeight=True, allowPOS=('vn', 'v'))
        for item in keywords:
            Comment_key.write(item[0] + ': ' + str(item[1]) + '\n')
            Comment_key.write('\n')
        Comment_key.write('Character: ' + '\n')
        keywords = jieba.analyse.textrank(raw_text, topK=10, withWeight=True, allowPOS=('nr'))
        for item in keywords:
            Comment_key.write(item[0] + ': ' + str(item[1]) + '\n')
            Comment_key.write('\n')
        Comment_key.write('Adj: ' + '\n')
        keywords = jieba.analyse.textrank(raw_text, topK=10, withWeight=True, allowPOS=('a'))
        for item in keywords:
            Comment_key.write(item[0] + ': ' + str(item[1]) + '\n')
            Comment_key.write('\n')
        Comment_key.close()





