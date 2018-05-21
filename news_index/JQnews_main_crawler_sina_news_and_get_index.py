# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:35:01 2018

@author: Richard10ZTZ
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import tushare as ts
from JQnews_get_news_index import get_news_index, decideEmo


'''输入初始新闻网页网址，爬取新闻到某一日期，'''
def get_news_index_list(website):
    driver = webdriver.PhantomJS(executable_path = 'E:\\Anaconda2\\phantomjs\\bin\\phantomjs.exe')
    driver.get(website)  
    result = []
    tempDate = ''
    tempRead = 0.0
    tempComment = 0.0
    tempTitle = ''
    tempScore = 0.0
    flagDate = 0
    while flagDate == 0: 

        #获取当前页新闻列表的源代码
        bs = BeautifulSoup(driver.page_source,'lxml')
        #每一条新闻
        for item in bs.find_all('div', class_='articleh'):
            
            tempresult =[]
            tempRead = item.find('span', class_='l1').string
            tempComment = item.find('span', class_='l2').string
            tempDate = item.find('span', class_='l6').string
            tempTitle = item.find('span', class_='l3').a.string
            tempScore = get_news_index(tempTitle)
            
            print '标题内容', tempTitle
            print '阅读数', tempRead
            print '评论数', tempComment 
            print '发表日期', tempDate
            print '正负性', tempScore    
            print 
            
            if '08-' in tempDate:
                print tempDate
                print '到日子了'
                flagDate = 1
                break
            if flagDate == 0:
                tempresult.append(tempDate)
                tempresult.append(tempTitle)
                tempresult.append(tempScore)
                tempresult.append(tempRead)
                result.append(tempresult)

        try:
            driver.find_element(By.LINK_TEXT, "下一页").click()
        except:
            print '没有下一页了'
     
        time.sleep(1)   
    return result


'''输入按时间收集的新闻、分数list，返回按天的df'''
def trans_result_to_allday_df(result):
    totalTime =[]
    onedayScore = 0.0
    alldayScore = []
    for idx, enty in enumerate(result):
        tempDate = add_years(enty[0])
        tempScore = float(enty[2]-0.5) # 正则化
        tempRead = int(enty[3])
        #输出有新闻的每一天的日期，单个新闻分数，阅读量，新闻分数计算
        #print tempDate, tempScore, tempRead, tempScore*tempRead
        tempDateR = datetime.datetime.strptime(tempDate, '%Y-%m-%d')
        if tempDateR in totalTime:
            onedayScore += tempRead*tempScore
        else:
            totalTime.append(tempDateR)
            if idx != 0: 
                alldayScore.append(onedayScore)
                onedayScore = tempRead*tempScore
            else:
                onedayScore = tempRead*tempScore
        
        if idx == len(result)-1:
            alldayScore.append(onedayScore)
        
    resultdf = pd.DataFrame({'Date':totalTime, 'NewScore':alldayScore})
    resultdf.set_index('Date', inplace=True)    

    return resultdf


def add_years(tempdate):
    if int(tempdate.split('-')[0]) >= 6:
        return '2017-'+tempdate
    else:
        return '2018-'+tempdate


if __name__=='__main__':
    
    SecID = 603019
    
    
    website = "http://guba.eastmoney.com/list,%s,1,f_1.html"%SecID
    '''爬取新闻并得到对应的，分别为时间，标题，正负性因子，阅读数'''
    result = get_news_index_list(website)
    '''对原始收集的result进行处理，得到时间序列'''
    resultdf = trans_result_to_allday_df(result)
    resultdf.plot()
    # 保存到策略路径
    resultdf.to_csv(u'D:/Applications2/JoinQuant-Desktop/USERDATA/.joinquant/notebook/85ac30828335a92fe694ad583030ea95/%dNewsScore.csv'%SecID)
    # 保存到研究路径
    resultdf.to_csv(u'D:/Applications2/JoinQuant-Desktop/USERDATA/%dNewsScore.csv'%SecID)
        

        