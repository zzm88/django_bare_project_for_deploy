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

    url = 'http://43.249.192.245:7777/get_phone?user=%s&password=%s&xmid=%s' % ('zzm88','1988104',ITEMID)
    if PHONENUM != '' :
        url = 'http://43.249.192.245:7777/get_zd_phone?user=%s&password=%s&xmid=%s&zd_phone=%s' % ('zzm88','1988104',ITEMID,PHONENUM)
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    response = requests.get(url=url, headers=header_dict).content
    if json.loads(response)['msg_code'] != "OK" :#TOKEN错误，重新登录
        # login()#登录
        response =json.loads(response)['mes'] #再次获取手机
    elif json.loads(response)['msg_code'] == "OK":#取号成功
        for key,value in json.loads(response)['mes'].iteritems():
            phone_number = key
            phone_token =  value
        return '%s|%s' % (phone_number,phone_token)

def getphone_token(ITEMID,PHONENUM=''):

    url = 'http://43.249.192.245:7777/get_phone?user=%s&password=%s&xmid=%s&zd_phone=%s' % ('zzm88','1988104',ITEMID,PHONENUM)
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    response = requests.get(url=url, headers=header_dict).content
    if json.loads(response)['msg_code'] != "OK" :#TOKEN错误，重新登录
        # login()#登录
        response =json.loads(response)['mes'] #再次获取手机
    elif json.loads(response)['msg_code'] == "OK":#取号成功
        for key,value in json.loads(response)['mes'].iteritems():
            phone_number = key
            phone_token =  value
        return {phone_number:phone_token}

def getsms(PHONE_TOKEN,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
#    http://43.249.192.245:7777/cx_message?user=账号&password=密码&token=手机号对应token
    WAIT = 60 # 接受短信时长60s
    
   
    url = 'http://43.249.192.245:7777/cx_message?user=%s&password=%s&token=%s' % ('zzm88','1988104',PHONE_TOKEN)
      
    response = requests.get(url=url, headers=header_dict).content
    json_repsonse = json.loads(response)
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and json_repsonse['mes'] == '' and json_repsonse['msg_code']=='OK': # 60秒内且未成功

        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content
        json_repsonse = json.loads(response)
        
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if json_repsonse['mes'] != '':# 若成功
        
       
        TIME = str(round(TIME2-TIME1, 1))

        d = {"time":TIME,"round":ROUND,"msg":json_repsonse['mes'] }
        
        return d
    else:
        print('获取短信超时，错误代码是')
        # print(response)
        print('循环数是'+ROUND)
        d = {"error":response,"round":ROUND}
        return d

def releasephone(ITEMID,PHONENUM):
    phone_and_token = getphone_token(ITEMID,PHONENUM)


    url = 'http://43.249.192.245:7777/sf_phone?user=zzm88&password=1988104&token=%s' % (PHONENUM)
    response = requests.get(url=url, headers=header_dict).content
    if json.loads(response)['msg_code'] == 'OK' : #成功释放
        # MOBILE1 = response.split('|')[1]
          
        response = u"成功释放"
    else:
        response = u'联系管理员，错误代号'+ str(json.loads(response)['code'])
       
    return response
# def releasephone(ITEMID,PHONENUM):

#     response = u"成功释放"
#     return response
