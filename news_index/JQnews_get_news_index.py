# -*- coding: utf-8 -*-
"""
Created on Tue May 08 15:14:16 2018

@author: Richard10ZTZ
"""
from JQnews_get_features_p import clean_text, makeFeatureVec
import gensim
from sklearn.externals import joblib

model = gensim.models.Word2Vec.load("../../data/wiki.zh.text.model")
index2word_set = model
fl = 400          
preclf = joblib.load('news_model.m')

def decideEmo(result):
    print result
    if result > 0.5 :
        return '正面新闻'
    else:
        return '负面新闻'
def get_news_index(sen):#, model, fl, index2word_set, preclf
    tempcleansen = clean_text(sen)
    tempX = makeFeatureVec(tempcleansen, model, fl, index2word_set)
    tempresult = preclf.predict(tempX.reshape(1, -1)) 
    return tempresult

if __name__ == '__main__':
    # 设置模型参数

    testsen1 = u'完成数千万A轮融资后，量化交易平台聚宽（JoinQuant）开始进军机构市场'
    testsen2 = u'优矿资不抵债，大面积裁员'
    print testsen1 
    print decideEmo(get_news_index(testsen1))
    print 
    
    print testsen2
    print decideEmo(get_news_index(testsen2))
   