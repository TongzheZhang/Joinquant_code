# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 14:29:57 2018

@author: Richard10ZTZ
"""

import tushare as ts
from snownlp import SnowNLP
import datetime
import time

def doSth():  
    # 
    print(u'这个程序要开始疯狂的运转啦')  
  
# 一般网站都是1:00点更新数据，所以每天凌晨一点启动  
def timerFun(s=0):  
    while True:  
        now = datetime.datetime.now()  
        # print(now.hour, now.minute)  
        if now.second == s:  
            print 'what a funk'
            doSth()
            time.sleep(60)  
     

if __name__=='__main__':
    #print 'I make the world!'
    #print ts.get_latest_news()
    #currentTime = datetime.datetime.now().strftime("%m-%d %H:%M")
    #threholdTime = datetime.datetime.now().strftime("%m-%d %H:%M")
    
    
    # 获取最新的前80条新闻
    news = ts.get_latest_news(top=80, show_content=True)
    afternews = news[news.time>=threholdTime]
    total_sen = 0
    # 情感分析，输出一个得分
    for i in range(0,len(afternews['title'])):
        print afternews['title'][i]
        tempOnepiece = SnowNLP(afternews['title'][i]).sentiments
        print tempOnepiece
        total_sen = total_sen + tempOnepiece
    print total_sen/len(news['title'])
    #threholdTime = currentTime
