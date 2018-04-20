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

if __name__=='__main__':

    driver = webdriver.PhantomJS(executable_path = 'E:\\Anaconda2\\phantomjs\\bin\\phantomjs.exe')
    driver.get("http://guba.eastmoney.com/list,603019.html")
    
    #初始化全局变量
    result = []
    everydaycount = 1
    sentcul = 0
    tempWtime = ''
    #driver.find_element(By.LINK_TEXT, "公司新闻").click()
    time.sleep(1)
    #根据哪天爬，就改哪天
    recordData = '04-11'
    # 180页，每个股票不同，要自己倒。。。这个倒到了2017年9月1日
    for i in range(0,180): 

        #获取当前页新闻列表的源代码
        bs = BeautifulSoup(driver.page_source,'lxml')
        
        #每一条帖子
        for item in bs.find_all('div', class_='articleh'):
            #特殊的公告贴不在我们的考虑范围内
            if item.find('em') == None:

                tempCont = item.a.string
                tempRead = item.find('span', class_='l1').string
                tempDis = item.find('span', class_='l2').string
                tempTime = item.find('span', class_='l5').string
                tempSent = SnowNLP(tempCont).sentiments
                
                if tempTime.split()[0] != recordData:
                    print '换了一天'
                    tempOnedaysent = sentcul/everydaycount
                    print '今天总情绪：', tempOnedaysent
                    sentcul = 0
                    everydaycount = 1
                    tempresult = [tempWtime, tempOnedaysent]
                    result.append(tempresult)
                
                if tempTime.split('-')[0] in ['04','03','02','01']:
                    tempWtime = '2018-' + tempTime.split()[0]
                if tempTime.split('-')[0] in ['09','10','11','12']:
                    tempWtime = '2017-' + tempTime.split()[0]


                print tempSent, tempCont, tempRead, tempRead, tempTime, tempWtime
                   
                sentcul += tempSent
                everydaycount += 1
                recordData = tempTime.split()[0]
        
        driver.find_element(By.LINK_TEXT, "下一页").click()
        time.sleep(3)
    
    name = ['date', 'sentiment']
    savefile = pd.DataFrame(columns=name, data=result)
    savefile.to_csv('E:/ZTZ/Work/joinquant/Joinquant_code/csvtest.csv')