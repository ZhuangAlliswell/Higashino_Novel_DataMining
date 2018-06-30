
"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

import os
import re
import jieba
import jieba.posseg as pseg
import jieba.analyse
import csv
import numpy as np
import matplotlib.pyplot as plt


seg_list_file_addr = os.listdir('D:\DataMiningCourse\神探伽利略系列')
print(seg_list_file_addr)
sentence_statistic = open('D:\DataMiningCourse\神探伽利略系列输出\\sentence_statistic.txt', 'w', encoding='utf-8', errors='ignore')
data_file = open('D:\DataMiningCourse\神探伽利略系列输出\\data_file.data', 'w', encoding='utf-8', errors='ignore')
sentence_style_list = []


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


dict_series_state = {}
dict_series_quest = {}
dict_series_rquest = {}
dict_series_active= {}
dict_series_passive = {}

for book in seg_list_file_addr:
    Quest_cnt = 0
    State_cnt = 0
    Reverse_Quest_cnt = 0
    Active_cnt = 0
    Passive_cnt = 0
    temp_style_list = []
    text_list = open('D:\DataMiningCourse\神探伽利略系列\\' + book, 'r', encoding='utf-8')
    text_list2 = open('D:\DataMiningCourse\\伽利略小说人物(1).txt', 'r', encoding='utf-8')
    sentence_output = open('D:\DataMiningCourse\神探伽利略系列输出\\' + book + '_sentence_output.txt', 'w', encoding='utf-8', errors='ignore')

    jieba.load_userdict(text_list2)
    temp_character = []
    dict_character_verb = {}
    dict_freq = {}
    dict_freq_v = {}
    dict_freq_adj = {}
    dict_freq_n = {}

    for line in text_list.readlines():
        if '？' in line:
            Quest_cnt += 1
        else:
            State_cnt += 1
        if ('难道' in line and '？' in line) or ('怎能' in line and '？' in line) or ('怎么' in line and '能' in line) or (
                '怎么' in line and '就' in line) or ('不' in line and '？' in line) or ('没有' in line and '？' in line):
            Reverse_Quest_cnt += 1
        else:
            Active_cnt += 1
        if '被' in line or ('受' in line and '所' in line) or ('为' in line and '所' in line):
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
                    if word.word in dict_freq_v:
                        dict_freq_v[word.word] += 1
                    else:
                        dict_freq_v[word.word] = 1

                if word.word in dict_freq:
                    dict_freq[word.word] += 1
                else:
                    dict_freq[word.word] = 1

                if word.flag == 'a':
                    if word.word in dict_freq_adj:
                        dict_freq_adj[word.word] += 1
                    else:
                        dict_freq_adj[word.word] = 1

                if word.flag == 'n':
                    if word.word in dict_freq_n:
                        dict_freq_n[word.word] += 1
                    else:
                        dict_freq_n[word.word] = 1

            if len(temp_character) > 1 and temp_action != '':
                dict_character_verb[temp_action] = temp_character[0] + temp_action + temp_character[1]
            sentence_output.write('\n')

    dict_freq_sorted = sorted(dict_freq.items(), key=lambda item: item[1], reverse=True)
    dict_freq_n_sorted = sorted(dict_freq_n.items(), key=lambda item: item[1], reverse=True)
    dict_freq_v_sorted = sorted(dict_freq_v.items(), key=lambda item: item[1], reverse=True)
    dict_freq_adj_sorted = sorted(dict_freq_adj.items(), key=lambda item: item[1], reverse=True)
    print(dict_freq_n_sorted)
    print(dict_freq_v_sorted)
    print(dict_freq_adj_sorted)

    sentence_statistic.write("书名：" + book + '\n')
    sentence_statistic.write('陈述句:' + str(State_cnt) + ';')
    sentence_statistic.write('问句:' + str(Quest_cnt) + ';')
    sentence_statistic.write('反问句:' + str(Reverse_Quest_cnt) + ';')
    sentence_statistic.write('主动句:' + str(Active_cnt) + ';')
    sentence_statistic.write('被动句:' + str(Passive_cnt) + ';')
    sentence_statistic.write('\n')
    data_file.write(str(State_cnt) + ',' + str(Quest_cnt) + ',' + str(Reverse_Quest_cnt) + ',' + str(Active_cnt) + ',' + str(Passive_cnt) + ',' + book)
    sentence_num = State_cnt + Quest_cnt + Reverse_Quest_cnt
    sentence_num2 = Active_cnt + Passive_cnt
    temp_style_list = [State_cnt / 1.0 / sentence_num, Quest_cnt / 1.0 / sentence_num,
                       Reverse_Quest_cnt / 1.0 / sentence_num, Active_cnt / 1.0 / sentence_num2,
                       Passive_cnt / 1.0 / sentence_num2]

    print(Quest_cnt)
    print(State_cnt)
    print(Reverse_Quest_cnt)
    print(Passive_cnt)
    print(Active_cnt)
    temp_style_list = [State_cnt, Quest_cnt, Reverse_Quest_cnt, Active_cnt, Passive_cnt]
    sentence_style_list.append(temp_style_list)

    text_list.close()
    text_list2.close()
    sentence_output.close()

    fig = plt.figure(1)
    ax1 = plt.subplot(111)
    data = np.array(temp_style_list)
    width = 0.5
    x_bar = np.arange(5)
    rect = ax1.bar(left=x_bar, height=data, width=width, color="lightblue")
    for rec in rect:
        x = rec.get_x()
        height = rec.get_height()
        ax1.text(x + 0.1, 1.02 * height, str(height))
    ax1.set_xticks(x_bar)
    ax1.set_xticklabels(("State", "Quest", "R_Quest", "Active", "Passive"))
    ax1.set_ylabel("Ratio")
    ax1.set_title(book + "句法结构")
    ax1.grid(True)
    ax1.set_ylim(0, 1)
    plt.show()

    book.replace('.txt', ' ', 2)
    csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + book + 'dict_freq_n_sorted.csv', 'w',
                   newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile)
    for i in range(len(dict_freq_n_sorted)):
        writer.writerow(dict_freq_n_sorted[i])
    csvFile.close()
    csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + book + 'dict_freq_v_sorted.csv', 'w',
                   newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile)
    for i in range(len(dict_freq_v_sorted)):
        writer.writerow(dict_freq_v_sorted[i])
    csvFile.close()
    csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + book + 'dict_freq_adj_sorted.csv', 'w',
                   newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile)
    for i in range(len(dict_freq_adj_sorted)):
        writer.writerow(dict_freq_adj_sorted[i])
    csvFile.close()

    dict_series_active[book] = Active_cnt / 1.0 / sentence_num2
    dict_series_passive[book] = Passive_cnt / 1.0 / sentence_num2
    dict_series_state[book] = State_cnt / 1.0 / sentence_num2
    dict_series_quest[book] = Quest_cnt / 1.0 / sentence_num2
    dict_series_rquest[book] = Reverse_Quest_cnt / 1.0 / sentence_num2

print(sentence_style_list)
data = np.array(sentence_style_list, dtype=float)
data_file.close()
sentence_statistic.close()

csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + 'series_active.csv', 'w',
               newline='')  # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile)
for key in dict_series_active:
    writer.writerow([key, dict_series_active[key]])
csvFile.close()

csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + 'series_passive.csv', 'w',
               newline='')  # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile)
for key in dict_series_passive:
    writer.writerow([key, dict_series_passive[key]])
csvFile.close()

csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + 'series_state.csv', 'w',
               newline='')  # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile)
for key in dict_series_state:
    writer.writerow([key, dict_series_state[key]])
csvFile.close()

csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + 'series_quest.csv', 'w',
               newline='')  # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile)
for key in dict_series_quest:
    writer.writerow([key, dict_series_quest[key]])
csvFile.close()

csvFile = open('D:\DataMiningCourse\神探伽利略系列输出\\' + 'series_rquest.csv', 'w',
               newline='')  # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile)
for key in dict_series_rquest:
    writer.writerow([key, dict_series_rquest[key]])
csvFile.close()
