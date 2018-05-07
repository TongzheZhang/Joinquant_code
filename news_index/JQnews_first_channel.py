# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:27:36 2017

@author: jrkj-shixi08
"""

import jieba
import numpy as np

'''
加载词表
'''
def createstoplist(stoppath):
    print('load corpus...')
    stoplist=[line.strip().decode('utf-8') for line in open(stoppath,'r').readlines()]
    #stopwords={}.fromkeys(stoplist)
    stopwords = set(stoplist)
    return stopwords

def firstchannel(sentence,posset,negset):
    words = list(jieba.cut(sentence.replace("\n", " "),cut_all=False))
    numpos = 0
    numneg = 0
    for word in words:
        if word in posset:
            numpos += 1
        elif word in negset:
            numneg += 1
    if numpos>numneg and numpos==1:
        return 1
    elif numneg<numpos and numneg==1:
        return 0
    else:
        return 2

if __name__ == '__main__':
    w = open('../Data/dat_p.txt')
    lines = w.readlines()
    posset = createstoplist('../Data/pos_corpus.txt')
    negset = createstoplist('../Data/neg_corpus.txt')
    jieba.load_userdict('../Data/final_corpus.txt')
    #print firstchannel("下跌幅度过大",posset,negset)
    #testsentence = "下跌幅度过大"
    y = np.load('../Data/y_p.npy')
    results = []
    y_r = []
    lines_r = []
    count = 0
    for i, line in enumerate(lines):
        result =  firstchannel(line,posset,negset)
        if result != 2:
            results.append(result)
            y_r.append(y[i])
            lines_r.append(line)
    for i in range(len(y_r)):
        if y_r[i] == results[i]:
            count += 1
        else:
            print lines_r[i],y_r[i],results[i] 
    print count
    