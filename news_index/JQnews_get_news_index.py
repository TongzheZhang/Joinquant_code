# -*- coding: utf-8 -*-
"""
Created on Tue May 08 15:14:16 2018

@author: Richard10ZTZ
"""
from JQnews_get_features_p import clean_text, makeFeatureVec
import gensim
from sklearn.externals import joblib

def decideEmo(result):
    if result == 1:
        return '正面新闻'
    else:
        return '负面新闻'

if __name__ == '__main__':
    # 设置模型参数
    model = gensim.models.Word2Vec.load("../../data/wiki.zh.text.model")
    index2word_set = model
    fl = 400
    preclf = joblib.load('news_model.m')
    
    
    testsen = u'完成数千万A轮融资后，量化交易平台聚宽（JoinQuant）开始进军机构市场'
    print testsen
    testcleansen = clean_text(testsen)
    print testcleansen
    testX = makeFeatureVec(testcleansen, model, fl, index2word_set)
    testresult = preclf.predict(testX.reshape(1, -1)) 
    print decideEmo(testresult)