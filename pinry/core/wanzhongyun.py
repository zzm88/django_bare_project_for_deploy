#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = 'Bb5f71b0abe411ea816200163e0007a2'

api = "http://to.banma1024.com"

def login():
    # url = 'http://xiangjiuer.cn/sms/api/login?username=API用户名&password=密码' % ('zzm88','1988104')    
    url = 'http://dev.wanzhongma.com/open/api/login?userName=%s&password=%s&json=1' % ('api-8zNeXR','1988104')    
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')

    global TOKEN 
    if json.loads(response)['code'] == '0': #登陆成功
        TOKEN = json.loads(response)['token'] 
    else:
        pass
    

# Create your tests here.
def getphone(ITEMID,PHONENUM=''):

    url = 'http://dev.wanzhongma.com/open/api/getPhone?token=%s&sid=%s&phone=%s&json=1' % (TOKEN,ITEMID,PHONENUM)
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    response = requests.get(url=url, headers=header_dict).content
    if json.loads(response)['code'] == 401 :#TOKEN错误，重新登录
        login()#登录
        response = getphone(TOKEN,ITEMID,PHONENUM) #再次获取手机
    elif json.loads(response)['code'] == 0:#取号成功
       return json.loads(response)['mobile']
    else:#取号成功
        response = json.loads(response)['code']
        return u'联系管理员%s' % (response)

def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    
   
    url = 'http://dev.wanzhongma.com/open/api/getMessage?token=%s&sid=%s&phone=%s&json=1' % (TOKEN,ITEMID,MOBILE)
      
    response = requests.get(url=url, headers=header_dict).content
    json_repsonse = json.loads(response)
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and json_repsonse['code'] != 0: # 60秒内且未成功
        if json_repsonse['code'] == 401: #TOKEN错误
            login()  #再登陆
        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content
        json_repsonse = json.loads(response)
        
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if json_repsonse['code'] == 0:# 若成功
        
        text = json_repsonse['RecvContent']
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
    url = 'http://dev.wanzhongma.com/open/api/cancelRecv?token=%s&sid=%s&phone=%s&json=1' % (TOKEN,ITEMID,PHONENUM)
    response = requests.get(url=url, headers=header_dict).content
    if json.loads(response)['code'] == 0 : #成功释放
        # MOBILE1 = response.split('|')[1]
          
        response = u"成功释放"
    else:
        response = u'联系管理员，错误代号'+ str(json.loads(response)['code'])
       
    return response
