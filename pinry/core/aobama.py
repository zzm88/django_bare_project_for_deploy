#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = '693f4780-6686-47f9-9c4a-00da4c9f906f-24537'


api_addresss = "http://api.aobama.co"
api = "1309269908"
password = "123456"
id = "zzm88aobama"

'''
http://api.aobama.co/api/login/?apiName=api-1309269908&password=123456&format=json
{"code":1,"msg":"success","data":"693f4780-6686-47f9-9c4a-00da4c9f906f-24537"}
'''
def login():  
    # url = ' http://api.aobama.co/api/login/?apiName=api-1309269908&password=123456&format=json
    #success response:
    #{"code":1,"msg":"success","data":"693f4780-6686-47f9-9c4a-00da4c9f906f-24537"}

    url =  "%s/api/login/?apiName=api-%s&password=%s&format=json" % (api_addresss,api,password)    
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')
    response = requests.get(url=url, headers=header_dict).content

    global TOKEN 
    if json.loads(response)['code'] == 1: #登陆成功
        TOKEN = json.loads(response)['token'] 
    else:
        pass
    




'''http://api.aobama.co/api/getPhone/?projectId=66658&card=虚拟&phone=&pre=&loop=0&token=693f4780-6686-47f9-9c4a-00da4c9f906f-24537&operate=zzm88aobaoma&format=json

{"code":1,"msg":"操作成功","data":"16573800365"}
'''
def getphone(ITEMID,PHONENUM=''):

    url = '%s/api/getPhone/?projectId=%s&card=虚拟&phone=%s&pre=&loop=0&token=%s&operate=&format=json' % (api_addresss,ITEMID,PHONENUM,TOKEN)
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    response = requests.get(url=url, headers=header_dict).content
    if json.loads(response)['code'] == 0 and json.loads(response)['msg'] == "账号或密码错误" :#TOKEN错误，重新登录
        login()#登录
        response = getphone(ITEMID,PHONENUM) #再次获取手机
        # response = json.loads(response)['reasonCode']
    elif json.loads(response)['code'] == 1:#取号成功
       return json.loads(response)['data']
    else:#取号失败
        response = json.loads(response)['msg']
        return u'联系管理员%s' % (response)
'''
http://api.aobama.co/api/getMessage/?projectId=66658&phone=16573800365&token=693f4780-6686-47f9-9c4a-00da4c9f906f-24537&format=json
{"code":0,"msg":"token已失效","data":""}
'''
def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    
   
    url = '%s/api/getMessage/?projectId=%s&phone=%s&token=%s&format=json' % (api_addresss,ITEMID,MOBILE,TOKEN)
      
    response = requests.get(url=url, headers=header_dict).content
    json_repsonse = json.loads(response)
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and json_repsonse['code'] != 1: # 60秒内且未成功
        print(json_repsonse)

        if json_repsonse['msg'] == "token已失效": #TOKEN错误
            login()  #再登陆
        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content
        json_repsonse = json.loads(response)
        
        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if json_repsonse['code'] == 1:# 若成功
        
        text = json_repsonse['data'] # change key name
        TIME = str(round(TIME2-TIME1, 1))

        d = {"time":TIME,"round":ROUND,"msg":text}
        
        return d
    else:
        print('获取短信超时，错误代码是')
        # print(response)
        print('循环数是'+ROUND)
        d = {"error":response,"round":ROUND}
        return d
'''
http://api.aobama.co/api/cancelRecv/?projectId=项目ID&phone=手机号码&token=登录返回token&format=json/html

'''
def releasephone(ITEMID,PHONENUM):
    url = '%s/api/cancelRecv/?projectId=%s&phone=%s&token=%s&format=json' % (api_addresss,ITEMID,PHONENUM,TOKEN)
    response = requests.get(url=url, headers=header_dict).content
    json_repsonse=json.loads(response)
    if json_repsonse['code'] == 1:# 若成功释放
        # MOBILE1 = response.split('|')[1]
          
        response = u"成功释放"
    else:
        response = u'联系管理员，错误代号'+ str(json.loads(response)['reasonCode'])
       
    return response
