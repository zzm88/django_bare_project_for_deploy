#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = Token.objects.get_or_create(id=1)[0].token

def login():
    url = 'http://api.xinma1.com:10000/login?uName=%s&pWord=%s' % ('zzm88','1988104')    
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')
    token = Token.objects.get_or_create(id=1)[0]
    token.token = response
    token.save()
    TOKEN = token.token
    

# Create your tests here.
def getphone(ITEMID,PHONENUM=''):
    
    url = '	 http://api.xinma1.com:10000/getPhone?ItemId=%s&token=%sPhone=%s' % (ITEMID,TOKEN,PHONENUM)
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    if 'False' not in response:
        response = response.split(';')[0]
        print response 
    elif "Session" in response:
        login()
        response = getphone(ITEMID,PHONENUM)
    else:
        print '获取TOKEN错误,错误代码'+response
    return response

def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    
   
    url = 'http://api.xinma1.com:10000/getMessage?token=%s&ItemId=%s&Phone=%s' % (TOKEN,ITEMID,MOBILE)
      
    response = requests.get(url=url, headers=header_dict).content.decode(encoding='utf-8')
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and not "MSG" in response:
        # 60秒内且未成功
        if "Session" in response:
            login()
        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content.decode(encoding='utf-8')
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if 'False' not in response:
        # 若成功
        text = response.split('&')[3]
        TIME = str(round(TIME2-TIME1, 1))
        #print(text)
        # print('耗费时长'+TIME+'s,循环数是'+ROUND)
        d = {"time":TIME,"round":ROUND,"msg":text}
        
        return d
    else:
        print('获取短信超时，错误代码是')
        print(response)
        print('循环数是'+ROUND)
        d = {"error":response,"round":ROUND}
        return d

def releasephone(ITEMID,PHONENUM):
    url = 'http://api.xinma1.com:10000/clearPhone?token=%s&phoneList=%s-%s' % (TOKEN,PHONENUM,ITEMID)
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    if 'False' not in response:
        # MOBILE1 = response.split('|')[1]
        print  
        response = "successfully release"+PHONENUM
    else:
        print 'error'+response
    return response
