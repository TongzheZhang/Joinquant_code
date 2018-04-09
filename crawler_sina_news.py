# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:02:17 2018
爬取新浪新闻
@author: Richard10ZTZ
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time
def get_links(driver):
    '''
    爬取链接并写入txt中
    '''
    t1 = time.time()
    try:
        driver.find_element(By.LINK_TEXT, "下一页").click()#每爬取完一页点击下一页
    except NoSuchElementException:
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "下5页").click()#有可能遇到没有下一页，尝试点击下5页
    time.sleep(1)
    bs = BeautifulSoup(driver.page_source)#不知道怎么用selenium直接解析出href。把selenium的webdriver调用page_source函数在传入BeautifulSoup中，就可以用BeautifulSoup解析网页了
    links = []
    for i in bs.findAll('a',href=re.compile("http://finance.sina.com.cn/chanjing/gsnews/.")):#用正则表达式找出所有需要的链接
        link = i.get('href')
        if link not in links:#去掉重复链接
            links.append(link)
            f.write(link+'\n')
    t2 = time.time()
    page_num = bs.find('span',{'class','pagebox_num_nonce'}).text#找出当前页数
    page_num = int(page_num)
    if page_num>4:
        return
    print('爬取完第%d页,用时%d秒'%(page_num,t2-t1))
    get_links(driver)
     
def get_text(links,path):
    '''
    解析出所需文本，第一个参数为链接列表，第二个为保存路径
    '''
    n=0
    for link in links:
        html = urlopen(link)
        bsObj = BeautifulSoup(html)
        temp = ''
        try:
            for link in bsObj.find("div",{'id':re.compile('artibody')}).findAll('p'):
                temp = temp+link.text.strip()#把每一段都拼接在一起
            print(temp[:31])
            path.write(temp+'\n')
            n+=1
            print('爬取完第%d篇'%n)
            print('\n')
        except (AttributeError,UnicodeEncodeError,UnicodeEncodeError):#这里的处理可能有点暴力
            continue
             
if True:#我把爬取的链接保存了下，所分成了两部，第一次爬取链接，第二次爬取文本 
    f = open('..\joinquantdata\hei.txt','w')
    driver = webdriver.PhantomJS()#如果phantomjs.exe所在路径没有加入环境变量，这里也可以直接把其路径作为参数传给PhantomJS()
    driver.get("http://finance.sina.com.cn/chanjing/")
    driver.find_element(By.LINK_TEXT, "公司新闻").click()
    time.sleep(2)
    get_links(driver)
    f.close()
    driver.close()
     
if True:#爬取文本 
    xl = open('..\joinquantdata\heiii.txt','w')
    with open('..\joinquantdata\heii.txt') as f:
        links = [link.strip() for link in f]
    get_text(links,xl)