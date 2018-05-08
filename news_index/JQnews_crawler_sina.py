# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:35:01 2018

@author: Richard10ZTZ
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time




if __name__=='__main__':

    driver = webdriver.PhantomJS(executable_path = 'E:\\Anaconda2\\phantomjs\\bin\\phantomjs.exe')
    driver.get(u"https://xueqiu.com/S/SH603019")
    
    
    result = []
    # driver.find_element(By.LINK_TEXT, u"新闻").click()
    time.sleep(1)
    recordData = ''
    for i in range(0,1): 

        #获取当前页新闻列表的源代码
        bs = BeautifulSoup(driver.page_source,'lxml')
        print bs
        #每一条新闻
        for item in bs.find_all('article', class_='timeline__item'):
            
            
            print item
            '''
            print item.find('div', class_='feed-card-time').string
            print item.a.string
            print item.find('div', class_='feed-card-txt').a.string
            print 
            temp = []
            temp.append(item.find('div', class_='feed-card-time').string)
            temp.append(item.a.string)
            temp.append(item.find('div', class_='feed-card-txt').a.string)
            result.append(temp)
            '''
   
            #driver.find_element(By.LINK_TEXT, "下一页").click()
        time.sleep(1)