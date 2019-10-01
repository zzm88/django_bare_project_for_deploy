#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = '4ee758e834e62ca14aefb5729e0a8ccc' 
	

# Create your tests here.
def getphone(ITEMID,PHONENUM=''):
    
    url = 'http://api.xinheyz.com/api/do.php?action=getPhone&sid=%s&token=%s&phone=%s' % (ITEMID,TOKEN,PHONENUM)
    MOBILE1 = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    if MOBILE1.split('|')[0] == 'success':
        MOBILE1 = MOBILE1.split('|')[1]
        print MOBILE1 
        
    else:
        print '获取TOKEN错误,错误代码'+MOBILE1
    return MOBILE1

def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    
   
    url = 'http://api.xinheyz.com/api/do.php?action=getMessage&sid=%s&token=%s&phone=%s' % (ITEMID,TOKEN,MOBILE)
      
    text1 = requests.get(url=url, headers=header_dict).content.decode(encoding='utf-8')
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1
    while (TIME2-TIME1) < WAIT and not text1.split('|')[0] == "1":
        time.sleep(5)
        text1 = requests.get(url=url, headers=header_dict).content.decode(encoding='utf-8')
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if text1.split('|')[0] == "1":
        text = text1.split('|')[1]
        TIME = str(round(TIME2-TIME1, 1))
        #print(text)
        # print('耗费时长'+TIME+'s,循环数是'+ROUND)
        d = {"time":TIME,"round":ROUND,"msg":text}
        
        return d
    else:
        print('获取短信超时，错误代码是')
        print(text1)
        print('循环数是'+ROUND)
        d = {"error":text1,"round":ROUND}
        return d

def releasephone(ITEMID,PHONENUM):
    url = 'http://api.xinheyz.com/api/do.php?action=cancelRecv&sid=%s&token=%s&phone=%s' % (ITEMID,TOKEN,PHONENUM)
    MOBILE1 = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    if MOBILE1.split('|')[0] == '1':
        MOBILE1 = MOBILE1.split('|')[1]
        print MOBILE1 
        
    else:
        print '获取TOKEN错误,错误代码'+MOBILE1
    return MOBILE1
