#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = 'd5dc3b7296a0da149eefa9b4ad9e6492'

api = "http://gateway.cszbdp.com/api2/"

def login():
    url = '	http://gateway.cszbdp.com/api2/login?member_no=%s&pwd=%s' % ('zzm88','123456a')    
    response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')
    response = response.strip('"') 
    global TOKEN 
    if response.split(':')[0] == '1': #登陆成功
        TOKEN = response.split(':')[1]
    else:
        pass

#测试链接    
# http://localhost:8000/getphone_new/188

# Create your tests here.
def getphone(ITEMID,PHONENUM=''):
    if PHONENUM != '':
        PHONENUM = '&phone=%s' % (PHONENUM)
    url = 'http://gateway.cszbdp.com/api2/getCardNo?token=%s&project_id=%s' % (TOKEN,ITEMID) + PHONENUM
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')
    response = requests.get(url=url, headers=header_dict).content
    response = response.strip('"') 
    if response.split(':')[1] == "token参数缺失" :#TOKEN错误，重新登录
       login()#登录
    if response.split(':')[0] == "0" :
        # login()#登录
        return response.split(':')[1] #失败则返回错误信息
    elif response.split(':')[0] == "1" : #取号成功
      
        phone_number = response.split(':')[1]
        return phone_number

def getphone_token(ITEMID,PHONENUM=''):

    url = 'http://yima.hbtfcc.com:7777/get_phone?user=%s&password=%s&xmid=%s&zd_phone=%s' % ('zzm88','1988104',ITEMID,PHONENUM)
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

def getsms(PHONENUM,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
#    http://yima.hbtfcc.com:7777/cx_message?user=账号&password=密码&token=手机号对应token
    WAIT = 60 # 接受短信时长60s
    
   
    url = 'http://gateway.cszbdp.com/api2/getSmsContent?token=%s&project_id=%s&card_no=%s&sms_seq=1' % (TOKEN,ITEMID,PHONENUM)
      
    response = requests.get(url=url, headers=header_dict).content
    response = response.strip('"') 
    if response.split(':')[1] == "身份验证失败，请重新登录" :#TOKEN错误，重新登录
       login()#登录
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and response.split(':')[0] == '0': # 60秒内且未成功

        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content
        response = response.strip('"') 
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if response.split(':')[0] == '1':# 若成功
        
       
        TIME = str(round(TIME2-TIME1, 1))

        d = {"time":TIME,"round":ROUND,"msg":response.split(':')[1]}
        
        return d
    else:
        print('获取短信超时，错误代码是')
        # print(response)
        print('循环数是'+ROUND)
        d = {"error":response,"round":ROUND}
        return d


# http://localhost:8000/release_new
def releasephone(ITEMID,PHONENUM):

    url = 'http://gateway.cszbdp.com/api2/releaseTimeoutCardNo?token=%s&project_id=%s&card_no=%s' % (TOKEN,ITEMID,PHONENUM)
    response = requests.get(url=url, headers=header_dict).content
    response = response.strip('"') 
    if  response.split(':')[0] == "1" : #成功释放
        # MOBILE1 = response.split('|')[1]
          
        response = u"成功释放"
    else:
        response = u'联系管理员，错误:'+  response.split(':')[1]
       
    return response
# def releasephone(ITEMID,PHONENUM):

#     response = u"成功释放"
#     return response
