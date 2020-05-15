#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = 'e8364b1268c4c3e34df01d9790b3be570e1bc882'

def login():
    # url = 'http://api.xinma1.com:10000/login?uName=%s&pWord=%s' % ('zzm88','1988104')    
    url = 'http://to.banma1024.com/api/do.php?action=loginIn&name=%s&password=%s' % ('api-113233-WIjNLBEXkfOz','1988104')    
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')

    global TOKEN 
    if response.split('|')[0] == '1': #登陆成功
        TOKEN = response.split('|')[1]
    else:
        pass
    

# Create your tests here.
def getphone(ITEMID,PHONENUM=''):
    
    url = 'http://to.banma1024.com/api/do.php?action=getPhone&sid=%s&token=%s&phone=%s' % (ITEMID,TOKEN,PHONENUM)
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    
    if response.split('|')[0] == "0" :#TOKEN错误，重新登录
        login()#登录
        response = getphone(ITEMID,PHONENUM) #再次获取手机
    elif response.split('|')[0] =="1":
       return  response.split('|')[1]

def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    
   
    url = 'http://api.banma1024.com/api/do.php?action=getMessage&sid=%s&phone=%s&token=%s' % (ITEMID,MOBILE,TOKEN)
      
    response = requests.get(url=url, headers=header_dict).content.decode(encoding='utf-8')
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and response.split('|')[0] =="0": # 60秒内且未成功
        if  response.split('|')[0] =="0" and "token" in response: #TOKEN错误
            login()  #再登陆
        
        time.sleep(3)
        response = requests.get(url=url, headers=header_dict).content.decode(encoding='utf-8')
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if response.split('|')[0]=='1':# 若成功
        
        text = response.split('|')[1]
        TIME = str(round(TIME2-TIME1, 1))

        d = {"time":TIME,"round":ROUND,"msg":text}
        
        return d
    else:
        print('获取短信超时，错误代码是')
        # print(response)
        print('循环数是'+ROUND)
        d = {"error":response,"round":ROUND}
        return d

def releasephone(ITEMID,PHONENUM):
    url = 'http://api.banma1024.com/api/do.php?action=cancelRecv&sid=%s&phone=%s&token=%s' % (ITEMID,PHONENUM,TOKEN)
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    if response.split('|')[0]=="1": #成功释放
        # MOBILE1 = response.split('|')[1]
        print  
        response = "successfully release"+PHONENUM
    else:
        print 'error'+response
    return response
