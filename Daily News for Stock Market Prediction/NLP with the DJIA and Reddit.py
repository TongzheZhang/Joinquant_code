# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 16:24:59 2018
OMG! NLP with the DJIA and Reddit
@author: Richard10ZTZ
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

data = pd.read_csv('own_data/Combined_News_DJIA.csv')

#print data.head()

train = data[data['Date'] < '2015-01-01']
test = data[data['Date'] > '2014-12-31']

example = train.iloc[3,10]
print(example)

example2 = example.lower()
print(example2)

example3 = CountVectorizer().build_tokenizer()(example2)
print(example3)

print pd.DataFrame([[x,example3.count(x)] for x in set(example3)], columns = ['Word', 'Count'])

trainheadlines = []
for row in range(0,len(train.index)):
    trainheadlines.append(' '.join(str(x) for x in train.iloc[row,2:27]))
    
    basicvectorizer = CountVectorizer()
basictrain = basicvectorizer.fit_transform(trainheadlines)
print basictrain.shape

basicmodel = LogisticRegression()
basicmodel = basicmodel.fit(basictrain, train["Label"])

testheadlines = []
for row in range(0,len(test.index)):
    testheadlines.append(' '.join(str(x) for x in test.iloc[row,2:27]))
basictest = basicvectorizer.transform(testheadlines)
predictions = basicmodel.predict(basictest)

print pd.crosstab(test["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])

basicwords = basicvectorizer.get_feature_names()
basiccoeffs = basicmodel.coef_.tolist()[0]
coeffdf = pd.DataFrame({'Word' : basicwords, 
                        'Coefficient' : basiccoeffs})
coeffdf = coeffdf.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
print coeffdf.head(10)
print coeffdf.tail(10)

'''2-gram方法'''
advancedvectorizer = CountVectorizer(ngram_range=(2,2))
advancedtrain = advancedvectorizer.fit_transform(trainheadlines)

print advancedtrain.shape

advancedmodel = LogisticRegression()
advancedmodel = advancedmodel.fit(advancedtrain, train["Label"])

testheadlines = []
for row in range(0,len(test.index)):
    testheadlines.append(' '.join(str(x) for x in test.iloc[row,2:27]))
advancedtest = advancedvectorizer.transform(testheadlines)
advpredictions = advancedmodel.predict(advancedtest)

print pd.crosstab(test["Label"], advpredictions, rownames=["Actual"], colnames=["Predicted"])

advwords = advancedvectorizer.get_feature_names()
advcoeffs = advancedmodel.coef_.tolist()[0]
advcoeffdf = pd.DataFrame({'Words' : advwords, 
                        'Coefficient' : advcoeffs})
advcoeffdf = advcoeffdf.sort_values(['Coefficient', 'Words'], ascending=[0, 1])
print advcoeffdf.head(10)