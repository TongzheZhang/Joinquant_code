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
    f = open(r'..\joinquantdata\newstitle.txt','w')
    driver = webdriver.PhantomJS(executable_path = 'E:\\Anaconda2\\phantomjs\\bin\\phantomjs.exe')
    driver.get("http://finance.sina.com.cn/chanjing/")
    
    
    result = []
    driver.find_element(By.LINK_TEXT, "公司新闻").click()
    time.sleep(1)

    for i in range(0,2):
        
        time.sleep(1)
        bs = BeautifulSoup(driver.page_source,'lxml')
        for item in bs.find_all('div', class_='feed-card-item'):
            print item.find('div', class_='feed-card-time').string
            print item.a.string
            print item.find('div', class_='feed-card-txt').a.string
            print 
            temp = []
            temp.append(item.find('div', class_='feed-card-time').string)
            temp.append(item.a.string)
            temp.append(item.find('div', class_='feed-card-txt').a.string)
            result.append(temp)
        driver.find_element(By.LINK_TEXT, "下一页").click()