# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 19:42:56 2017

@author: jrkj-shixi08
"""

import xlrd  
import jieba 
import numpy as np
import gensim
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from snownlp import SnowNLP
import jieba.posseg as pseg

'''
加载停用词表
'''
def createstoplist(stoppath):
    #print('load stopwords...')
    stoplist=[line.strip() for line in open(stoppath,'r').readlines()]
    stopwords={}.fromkeys(stoplist)
    return stopwords

def isAlpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False

def clean_text(sentence):
    #载入词库，如果出现词库中短语，则作为一个词语
    #stopwords=createstoplist('D:\ZTZ\Data\stop_words.txt')        
    newsentence = " "
    #使用结巴分词精准模式 or snownlp
    words = list(pseg.cut(sentence.replace("\n", " ")))
    #words = SnowNLP(sentence.replace("\n", " ")).tags
    for word in words:
        
        #去掉和英文,可以添加长度小于1的词:#词性为动词
        #if word[1] == 'v' \
        #V = ['v','vg','vn','vd']
        if isAlpha(word.word)==False \
        and word.word!='\t' \
        and len(word.word)>1 \
        and not word.word.isdigit():
            newsentence +=  word.word+' '
    #print newsentence
    return newsentence

'''输入一条以空格分开的文本，输出该文本的句向量'''
def makeFeatureVec(review, model, num_features, index2word_set):
    words = review.split(' ')
    featureVec = np.zeros((num_features,),dtype="float32")
    nwords = 0.0000001    
    for word in words:
        #改过，没测试过
        if type(word) != unicode: word = unicode(word, "utf-8")
        if word in index2word_set:
            nwords += 1.
            featureVec = np.add(featureVec,model[word])
    featureVec = np.divide(featureVec, nwords)
    return featureVec


'''输入多条文本，输出多条句向量'''
def getAllFeatureVecs(reviews, model, num_features, index2word_set):
    counter = 0
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    for review in reviews:
        reviewFeatureVecs[counter] = makeFeatureVec(review, model, num_features, index2word_set)
        counter += 1
    return reviewFeatureVecs
 
if __name__ == "__main__":

    #jieba.load_userdict('../Data/wiki_corpus.txt')
    workbook = xlrd.open_workbook('../../data/ZTZ_labeled_data_output.xlsx')  
    booksheet = workbook.sheet_by_index(0)         #用索引取第一个sheet   
    '''一些表格操作'''
    #cell = booksheet.cell_value(1,0) #读单元格数据   
    #row = booksheet.row_values(0) #读一行数据  
    #print "表单名称:", workbook.sheet_names()#查看所有sheet
    #print "表单数量:", workbook.nsheets
    clean_train_reviews = []
    y = []
    '''写入文本'''
    wfile1 ='../../data/dat_after_process_p.txt'
    wfile2 ='../../data/dat_p.txt'
    wf1 = open(wfile1,'wb')
    #wf2 = open(wfile2,'wb')
    for i in range(1, booksheet.nrows):
        #print 'Before:', booksheet.row_values(i)[1], booksheet.row_values(i)[2]
        tempclean = clean_text(booksheet.row_values(i)[1])
        wf1.write(tempclean.encode('utf8')+'\t'+'%d'%(booksheet.row_values(i)[2])+'\n')
        #wf2.write(booksheet.row_values(i)[1].replace("\n", " ").replace("\r", " ").encode('utf8')+'\n')
        clean_train_reviews.append(tempclean)
        y.append(booksheet.row_values(i)[2])
        #print 'After:', clean_text(booksheet.row_values(i)[1])
        if i%1000==0: print i
     
    '''得到句特征'''
    model = gensim.models.Word2Vec.load("../../data/wiki.zh.text.model")
    index2word_set = model# set(model.index2word)   
    fl = 400
    X = getAllFeatureVecs(clean_train_reviews, model, fl, index2word_set)
    
    '''保存数据特征'''
    np.save("../../data/X_p.npy", X)
    np.save("../../data/y_p.npy", y)
   
         