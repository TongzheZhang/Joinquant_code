# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:35:01 2018

@author: Richard10ZTZ
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import tushare as ts
from JQnews_get_news_index import get_news_index, decideEmo



if __name__=='__main__':

    driver = webdriver.PhantomJS(executable_path = 'E:\\Anaconda2\\phantomjs\\bin\\phantomjs.exe')
    driver.get("http://guba.eastmoney.com/list,603019,1,f.html")
    

    
    result = []
    time.sleep(1)
    recordData = ''
    for i in range(0,1): 

        #获取当前页新闻列表的源代码
        bs = BeautifulSoup(driver.page_source,'lxml')
        #每一条新闻
        for item in bs.find_all('div', class_='articleh'):
            
            tempresult =[]
            #print item.find('span', class_='l1').string
            #print item.find('span', class_='l2').string
            #print item.find('span', class_='l6').string
            temptitle = item.find('span', class_='l3').a.string
            tempresult.append(temptitle)
            tempresult.append(get_news_index(temptitle))
            result.append(tempresult)
        driver.find_element(By.LINK_TEXT, "下一页").click()
        time.sleep(1)
        