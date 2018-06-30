
"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

import jieba
import os
import jieba.posseg as pseg
import jieba.analyse
from aip import AipNlp
import csv
from time import sleep

# 定义常量
APP_ID = '10582984'
API_KEY = 'ZSifoOGYo7O8cf4FUkRNrxuL'
SECRET_KEY = 'BpjTGC2mPKxouiIKtprxsuEsrypcv4tj '
# 初始化AipNlp对象
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
posi, nega  = [] ,[]

main_file_addr = 'D:\DataMiningCourse\爬虫结果'
sub_file_list = os.listdir(main_file_addr)
print(sub_file_list)

output_addr = 'D:\DataMiningCourse\爬虫结果分析\\'

for sub_file in sub_file_list[12:]:
    print('sub_file: ' + sub_file)
    text_file_list = os.listdir(main_file_addr + '\\' + sub_file)
    print(text_file_list)
    try:
        text = open(main_file_addr + '\\' + sub_file + '\\' + 'short_comments.txt', 'r')
        csvFile = open(output_addr + sub_file + '.csv', 'w', newline='')
        writer = csv.writer(csvFile)

        raw_text = text.read()
        keywords = jieba.analyse.textrank(raw_text, topK=20, withWeight=True, allowPOS=('ns', 'n', 'v', 'a'))

        for item in keywords:
            writer.writerow([item[0], item[1]])
    except:
        pass

    text2 = open(main_file_addr + '\\' + sub_file + '\\' + 'short_comments.txt', 'r').readlines()
    for line in text2:
        if ("==============" not in line) and ('[书籍]' not in line) and (line != '\n'):
            print(line)
            try:
                result = aipNlp.sentimentClassify(line)
            except:
                sleep(2)
                result = aipNlp.sentimentClassify(line)

            for item in result['items']:
                print(item)
                writer.writerow([item['positive_prob']])
    csvFile.close()


