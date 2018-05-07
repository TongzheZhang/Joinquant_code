# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 15:39:48 2017

@author: jrkj-shixi08
"""

from sklearn import svm
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn import neighbors
import time
from sklearn.externals import joblib
import random
from sklearn.grid_search import GridSearchCV


if __name__ == "__main__":
    '''计时开始'''
    #starttime = time.clock()
    #print "start time is:",starttime
 
    #载入所有特征和标记
    X = np.load('../Data/X_p.npy')#X = np.load('../Data/X_PCA.npy')
    y = np.load('../Data/y_p.npy')
    X_pos = []
    X_neg = []
    
    for i, label in enumerate(y):
        if label==1:
            X_pos.append(X[i])
        else:
            X_neg.append(X[i])
    X_pos_down = random.sample(X_pos, len(X_neg))
    ypos = np.ones(len(X_neg))
    yneg = np.zeros(len(X_neg))
    y_new = np.concatenate((ypos, yneg), axis=0)
    X_new = np.array(X_pos_down + X_neg)
    
    #定义分类器
    clf = svm.SVC(C=4.7, kernel = 'rbf')  #6.30957344480192986
    '''
    #scoring 可以是 'precision_macro' or 'recall_macro' or ' f1_macro']
    scores = cross_val_score(clf, X, y, cv=3, scoring = 'precision_macro')
    print "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
    scores = cross_val_score(clf, X, y, cv=3, scoring = 'recall_macro')
    print "Recall: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
    '''
    '''自己分训练集和测试集'''
    print '超参数搜索后的测试结果(7/3分)：'
    for i in range(3):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=i)
        clf.fit(X_train, y_train)
        print '第',i+1,'次测试',clf.score(X_test, y_test)
    print '超参数搜索后的测试结果(全样本)：'
    clf.fit(X, y)
    print clf.score(X, y)
    
    '''测试单一新闻标题'''
    '''
    clf.fit(X, y)  # training the svc model  
    result1 = clf.predict(X[5].reshape(1, -1))   
    result2 = clf.predict(X[-5].reshape(1, -1)) 
    print result1, result2 
    '''
    
    #elapsed = (time.clock() - starttime)
    #print "Time used:",elapsed/60,"mins"
    '''
    clf = svm.SVC()
    para = {'C':np.arange(4,6,0.1),'kernel':['rbf']}
    gs = GridSearchCV(clf, para, verbose=2,refit=True,cv=3,n_jobs = -1)
    gs.fit(X,y)
    print gs.score(X,y)
    print gs.best_params_,gs.best_score_
    '''