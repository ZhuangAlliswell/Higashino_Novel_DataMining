
"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

from aip import AipNlp
import os
import re
import csv
from time import sleep

file_addr = os.listdir('D:\DataMiningCourse\神探伽利略系列gbk')
print(file_addr)
motion_analyse_output_addr = 'D:\DataMiningCourse\神探伽利略系列输出\\'
# motion_analyse_output = open('D:\DataMiningCourse\加贺系列输出\\motion_analyse.txt', 'w', encoding='utf-8', errors='ignore')

# 定义常量
APP_ID = '10582984'
API_KEY = 'ZSifoOGYo7O8cf4FUkRNrxuL'
SECRET_KEY = 'BpjTGC2mPKxouiIKtprxsuEsrypcv4tj '
# 初始化AipNlp对象
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
posi, nega  = [] ,[]


for book in file_addr[10:]:
    motion_analyse_output = open(motion_analyse_output_addr + book + '_motion_analyse.txt', 'w', encoding='utf-8', errors='ignore')
    motion_analyse_output_csv = open(motion_analyse_output_addr + book + '_motion_analyse.csv', 'w', newline='')
    writer = csv.writer(motion_analyse_output_csv)
    text_list = open('D:\DataMiningCourse\神探伽利略系列gbk\\' + book, 'r', encoding='gbk')
    text = text_list.readlines()
    list_motion = []
    print(book)
    for line in text:
        if line != '\n':
            try:
                result = aipNlp.sentimentClassify(line)
            except:
                sleep(2)
                result = aipNlp.sentimentClassify(line)
        for item in result['items']:
                # print('原文: ' + result['text'] + '  ')
                motion_analyse_output.write('原文: ' + result['text'] + '  ')
                list_motion = [item['positive_prob'], item['negative_prob'], item['confidence'], item['sentiment']]
                print(list_motion)
                for issue in item:
                    print('{0}: {1:.6f}'.format(issue, item[issue]))
                    motion_analyse_output.write('{0}: {1:.6f}'.format(issue, item[issue]) + '  ')
                motion_analyse_output.write('\r\n ')
                writer.writerow(list_motion)
    motion_analyse_output.close()
    motion_analyse_output_csv.close()
