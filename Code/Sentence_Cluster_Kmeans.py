# !/usr/bin/python
# -*- coding:utf-8 -*-

"""
Created on Fri Jan. 5 11:25:14 2018

@author: Estar
"""

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin


def show_accuracy(a, b, tip):
    acc = a.ravel() == b.ravel()
    print (tip + '正确率：', np.mean(acc))


def book_series(s):
    it = {'《再一个谎言》之寒冷的灼热.txt': 0, '东野圭吾《麒麟之翼》.txt': 0, '恶意.txt': 0, '我杀了他.txt':0, '新参者.txt':0, '毕业前杀人游戏.txt':0, '沉睡的森林.txt':0, '祈祷落幕时.txt':0, '红手指.txt':0, '谁杀了她.txt':0,
          '东野圭吾_嫌疑犯X的献身.txt': 1, '伽利略的苦恼01 坠落 .txt': 1, '伽利略的苦恼02 操纵.txt': 1, '伽利略的苦恼03 密室.txt': 1, '伽利略的苦恼04 指示.txt': 1, '伽利略的苦恼05 扰乱.txt': 1, '侦探伽利略01 燃烧.txt': 1,
          '侦探伽利略02 映现.txt': 1, '侦探伽利略03 坏死.txt': 1, '侦探伽利略04 爆裂.txt': 1, '侦探俱乐部01 伪装之夜.txt': 1, '侦探伽利略04 爆裂.txt': 1, '侦探俱乐部02 疯狂的电击.txt': 1, '侦探俱乐部03 少女委托人.txt': 1, '侦探俱乐部04 伊豆旅馆的神秘案.txt': 1,
          '侦探俱乐部05 玫瑰与匕首.txt': 1, '圣女的救济.txt': 1, '盛夏的方程式.txt': 1, '禁忌游戏01 透视.txt': 1, '禁忌游戏02 曲球.txt': 1, '禁忌游戏03 恋波.txt': 1, '禁忌魔术04 猛射.txt': 1, '虚像的小丑01 幻惑.txt': 1, '虚像的小丑02 听心.txt': 1,
          '虚像的小丑03 伪装.txt': 1, '虚像的小丑04 演技.txt': 1}
    return it[s]


def book_series2(s):
    it = {b'a': 0, b'b': 1}
    return it[s]


# iris_feature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'

if __name__ == "__main__":
    path = 'D:\DataMiningCourse\\data_file.data'  # 数据文件路径
    path2 = 'D:\DataMiningCourse\\data_file2.data'  # 数据文件路径
    data = np.loadtxt(path2, dtype=float, delimiter=',', converters={5: book_series2})
    print(data)
    x, y = np.split(data, (5,), axis=1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
    clf = KMeans(n_clusters=2, init='k-means++')
    clf.fit(x_train, y_train.ravel())
    y_hat = clf.predict(x_test)
    y_test=y_test.ravel()
    m_hat = np.array([np.mean(x_test[y_hat == i], axis=0) for i in range(2)])
    m = np.array([np.mean(x_test[y_test == i], axis=0) for i in range(2)])
    print(m_hat)
    print(m)
    order = pairwise_distances_argmin(m, m_hat, axis=1, metric='euclidean')
    print (order)
    n_sample = y_test.size
    n_types = 2
    change = np.empty((n_types, n_sample), dtype=np.bool)
    for i in range(n_types):
        change[i] = y_hat == order[i]
    for i in range(n_types):
        y_hat[change[i]] = i
    acc = u'准确率：%.2f%%' % (100 * np.mean(y_hat == y_test))
    print (acc)


