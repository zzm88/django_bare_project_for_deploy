#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI0MzI0NSIsImlhdCI6MTU5MTk1NzAzMiwiZXhwIjoxNTk4MDA1MDMyfQ.jOFn8BCY9mOsYsSzOSeyxrdg8STnDrBBnzhOOIVCrtVk_4_eoxen5oqeXmLiGLoXMfJsmE8_KLYxbMgXEggPCw'

apiAccount = "a0bca578-4ea2-4e4e-b4d5-69068aef7170"




'''
[返回信息]:
成功统一返回：{result: "成功", token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZWI0ZjUwN2VlYTIzZjc2YzMzZmFjY2UiLCJhcGlBY2NvdW50IjoiZWFhOGNkOWEtZTc5Mi00YjUxLWJlMzEtZTQ5YTAyNzA3MDI3IiwiaWF0IjoxNTg4OTE3NjE4fQ.CRe9svfuBLIYeN45qJ2raJIPbQ6H1wc-YCgGbiQjpYA"} 
失败统一返回：{result: "失败", reason: 失败原因, reasonCode: 失败代码}

'''
def login():
    # url = 'http://xiangjiuer.cn/sms/api/login?username=API用户名&password=密码' % ('zzm88','1988104')    
    url = 'http://api.yumoyumo.com/api/yhdl?password=%s&apiAccount=%s' % ('feizhu123456','a0bca578-4ea2-4e4e-b4d5-69068aef7170')    
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')
    response = requests.get(url=url, headers=header_dict).content

    global TOKEN 
    if json.loads(response)['result'] == '成功': #登陆成功
        TOKEN = json.loads(response)['token'] 
    else:
        pass
    




'''
[返回信息]：
接码项目成功返回: {result: "成功", "number": [获取的号码] }
发码项目成功返回: {result: "成功", "availableReceiver": [可供发送的目标号码] ,"number": 获取的号码 }
失败返回: {result: "失败", reason: 失败原因, reasonCode: 失败代码}
'''
def getphone(ITEMID,PHONENUM=''):

    url = 'http://api.yumoyumo.com/api/yhqh_s?token=%s&id=%s&pingtaika=1&number=%s' % (TOKEN,ITEMID,PHONENUM)
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    response = requests.get(url=url, headers=header_dict).content
    if json.loads(response)['result'] == '失败' and json.loads(response)['reasonCode'] == 101 :#TOKEN错误，重新登录
        login()#登录
        response = getphone(ITEMID,PHONENUM) #再次获取手机
        # response = json.loads(response)['reasonCode']
    elif json.loads(response)['result'] == "成功":#取号成功
       return json.loads(response)['number']
    else:#取号失败
        response = json.loads(response)['reasonCode']
        return u'联系管理员%s' % (response)

def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    
   
    url = 'http://api.yumoyumo.com/api/yhjm?token=%s&id=%s&number=%s&apiAccount=%s' % (TOKEN,ITEMID,MOBILE,apiAccount)
      
    response = requests.get(url=url, headers=header_dict).content
    json_repsonse = json.loads(response)
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and json_repsonse['result'] != '成功': # 60秒内且未成功
        if json_repsonse['reasonCode'] == "101": #TOKEN错误
            login()  #再登陆
        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content
        json_repsonse = json.loads(response)
        
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if json_repsonse['result'] == "成功":# 若成功
        
        text = json_repsonse['smsContent']
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
    url = 'http://api.yumoyumo.com/api/yhsf?token=%s&id=%s&number=%s' % (TOKEN,ITEMID,PHONENUM)
    response = requests.get(url=url, headers=header_dict).content
    json_repsonse=json.loads(response)
    if json_repsonse['result'] == "成功":# 若成功释放
        # MOBILE1 = response.split('|')[1]
          
        response = u"成功释放"
    else:
        response = u'联系管理员，错误代号'+ str(json.loads(response)['reasonCode'])
       
    return response
