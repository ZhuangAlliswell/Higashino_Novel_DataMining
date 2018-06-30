
"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

import os
import jieba
import jieba.posseg as pseg
import jieba.analyse
import csv

seg_list_file_addr = os.listdir('D:\DataMiningCourse\加贺恭一郎系列')
seg_list_file_addr2 = os.listdir('D:\DataMiningCourse\神探伽利略系列')
print(seg_list_file_addr)
output_addr = 'D:\DataMiningCourse\加贺系列权重输出\\'
output_addr2 = 'D:\DataMiningCourse\伽利略系列权重输出\\'

for book in seg_list_file_addr:
    text_file = open('D:\DataMiningCourse\加贺恭一郎系列\\' + book, 'r', errors='ignore')
    # text_file = open('D:\DataMiningCourse\神探伽利略系列\\' + book, 'r', encoding='utf-8', errors='ignore')
    csv_File = open(output_addr + book + '.csv', 'w', newline='')
    writer = csv.writer(csv_File)

    raw_text = text_file.read()
    writer.writerow(['ns'])
    keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('ns'))
    for item in keywords:
        writer.writerow([item[0], item[1]])
    writer.writerow(['n'])
    keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('n'))
    for item in keywords:
        writer.writerow([item[0], item[1]])
    writer.writerow(['v & vn & vd'])
    keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('v', 'vn', 'vd'))
    for item in keywords:
        writer.writerow([item[0], item[1]])
    writer.writerow(['a'])
    keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('a'))
    for item in keywords:
        writer.writerow([item[0], item[1]])
    writer.writerow(['nt'])
    keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('nt'))
    for item in keywords:
        writer.writerow([item[0], item[1]])
    writer.writerow(['nr'])
    keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('nr'))
    for item in keywords:
        writer.writerow([item[0], item[1]])
    writer.writerow(['t'])
    keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('t'))
    for item in keywords:
        writer.writerow([item[0], item[1]])
    csv_File.close()
