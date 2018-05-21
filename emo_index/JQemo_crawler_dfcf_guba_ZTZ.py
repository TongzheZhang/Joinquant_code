# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:14:45 2018
爬取东方财富股吧帖子并NLP，得出情绪时间序列
东方财富的帖子 阅读，评论，标题，作者，发表日期，最后更新
我们这里只爬取 标题，阅读，评论，最后更新
@author: Richard10ZTZ
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time
from snownlp import SnowNLP
import pandas as pd
import time

def add_year(tempTime):
    if tempTime.split('-')[0] in ['08','07','06','05','04','03','02','01']:
        tempWtime = '2018-' + tempTime.split()[0]
    if tempTime.split('-')[0] in ['09','10','11','12']:
        tempWtime = '2017-' + tempTime.split()[0]
    return tempWtime

def get_emo_initial_result(stockcode):
    print 'begin collect emo'
    driver = webdriver.PhantomJS(executable_path = 'E:\\Anaconda2\\phantomjs\\bin\\phantomjs.exe')
    driver.get("http://guba.eastmoney.com/list,%d.html"%stockcode)
    
    #初始化全局变量
    result = []
    everydaycount = 1
    sentcul = 0
    tempWtime = ''
    #driver.find_element(By.LINK_TEXT, "公司新闻").click()
    time.sleep(1)
    #根据哪天爬，就改哪天
    recordDate = time.strftime('%m-%d',time.localtime(time.time()))
    
    flagDate = 0
    t = 0
    while flagDate == 0: 

        #获取当前页新闻列表的源代码
        bs = BeautifulSoup(driver.page_source,'lxml')
        
        #每一条帖子
        for item in bs.find_all('div', class_='articleh'):
            #特殊的公告贴不在我们的考虑范围内
            if item.find('em') == None and flagDate == 0:
                tempCont = item.a.string # 帖子标题
                tempRead = item.find('span', class_='l1').string # 阅读数
                tempDis = item.find('span', class_='l2').string # 讨论数
                tempTime = item.find('span', class_='l5').string # 最后更新的时间
                tempSent = SnowNLP(tempCont).sentiments
                if tempTime.split()[0] != recordDate:
                    #print '下一天'
                    tempOnedaysent = sentcul/everydaycount
                    #print recordDate, '总情绪：', tempOnedaysent
                    sentcul = 0
                    everydaycount = 1
                    tempresult = [tempWtime, tempOnedaysent]
                    result.append(tempresult)
                # 和百度因子同周期，到17年9月
                if tempTime.split('-')[0] == '08':
                    print '结束了！！！！！！！'
                    flagDate = 1
                    break
                tempWtime = add_year(tempTime)
                #print tempSent, tempCont, tempRead, tempRead, tempTime, tempWtime
                sentcul += tempSent
                everydaycount += 1
                recordDate = tempTime.split()[0]
        driver.find_element(By.LINK_TEXT, "下一页").click()
        time.sleep(5)
        print '%d page'%t
        t = t + 1
    name = ['date', 'sentiment']
    savefile = pd.DataFrame(columns=name, data=result)
    print 'end collect emo'
    return savefile

if __name__=='__main__':
    stockcode = 603019
    result = get_emo_initial_result(stockcode)
    result.to_csv('E:/ZTZ/Work/joinquant/Joinquant_code/emo_index/csvtest.csv')