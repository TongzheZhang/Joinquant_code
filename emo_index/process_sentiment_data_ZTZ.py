# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 10:28:44 2018
对原始的情绪因子的时间序列进行处理
@author: Richard10ZTZ
"""

import pandas as pd
from sklearn import preprocessing

def ES(sentArray, alpha):
    sentArrayES = []
    sentArrayES.append((sentArray[0]+sentArray[1]+sentArray[2])/3)
    for i in range(1, len(sentArray)):
        tempS = alpha*sentArray[i] + (1-alpha)*sentArrayES[-1]
        sentArrayES.append(tempS)
    return sentArrayES


if __name__ == '__main__':
    sent = pd.read_csv('603019sent.csv')
    
    sent.drop('Unnamed: 0',axis=1, inplace=True)
    sent = sent.iloc[::-1][:-1].reset_index(drop=True)  
    print '平均情绪：', sent.describe()['sentiment']['mean']
    
    sentArray = sent['sentiment'].values
    sent_scale =  preprocessing.scale(sentArray)
    sent['sent_scale']=sent_scale
    print '平均情绪_scale：', sent.describe()['sent_scale']['mean']
    
    
    sentArrayES = ES(sentArray, 0.5)
    sent['sent_ES']=sentArrayES
    print '平均情绪_ES：', sent.describe()['sent_ES']['mean']
    
    sent.index = sent['date'].tolist()
    sent.drop('date',axis=1, inplace=True)
    sent['sent_ES'].plot()
    
    sent.to_csv('603019sent_processed.csv')
    