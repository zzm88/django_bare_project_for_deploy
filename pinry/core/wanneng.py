#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = 'E78BAC86FF6B4313AFE9F5A0E170D4AF'


api_address = "http://api.wannengjm.com:6688/webapi/"
api = "1309269908"
password = "Zzm123456"
id = "Zzm123456"

'''
login()
    http://api.wannengjm.com:6688/webapi/login?uname=Zzm123456&upwd=Zzm123456
    "1|E78BAC86FF6B4313AFE9F5A0E170D4AF"
getphone()
    http://api.wannengjm.com:6688/webapi/GetPhone?ukey=E78BAC86FF6B4313AFE9F5A0E170D4AF&bid=2148
    "1|16533771701"

getsms()
    http://api.wannengjm.com:6688/webapi/GetMessage?ukey=E78BAC86FF6B4313AFE9F5A0E170D4AF&bid=2148&phone=16517682141
    http://api.wannengjm.com:6688/webapi/GetMessage?ukey=%s&bid=%s&phone=%s

release()
    http://api.wannengjm.com:6688/webapi/CancelRecv?&ukey=E78BAC86FF6B4313AFE9F5A0E170D4AF&bid=2148&phone=16521732865
    "1|释放操作成功"
'''

def login():  
    # url = ' http://api.aobama.co/api/login/?apiName=api-1309269908&password=123456&format=json
    #success response:
    #{"code":1,"msg":"success","data":"693f4780-6686-47f9-9c4a-00da4c9f906f-24537"}

    url =  "%slogin?uname=%s&upwd=%s" % (api_addresss,id,password)    
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')
    response = requests.get(url=url, headers=header_dict).content.strip('"')

    global TOKEN 
    if response.split('|')[0] == "1": #登陆成功
        TOKEN = response.split('|')[1]
    else:
        pass
    




'''http://api.aobama.co/api/getPhone/?projectId=66658&card=虚拟&phone=&pre=&loop=0&token=693f4780-6686-47f9-9c4a-00da4c9f906f-24537&operate=zzm88aobaoma&format=json

{"code":1,"msg":"操作成功","data":"16573800365"}
'''


def getphone(ITEMID,PHONENUM=''):

    url = '%sGetPhone?ukey=%s&bid=%s' % (api_address,TOKEN,ITEMID)
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    response = requests.get(url=url, headers=header_dict).content.strip('"').split("|")
    key= response[0]
    value = response[1]

    if  key == "0" and value == "身份验证失败，请重新登录" :#TOKEN错误，重新登录
        login()#登录
        response = getphone(ITEMID,PHONENUM) #再次获取手机
        # response = json.loads(response)['reasonCode']
    elif key == "1":#取号成功
       return value
    else:#取号失败
        response = value
        return u'联系管理员%s' % (response)
'''
http://api.aobama.co/api/getMessage/?projectId=66658&phone=16573800365&token=693f4780-6686-47f9-9c4a-00da4c9f906f-24537&format=json
{"code":0,"msg":"token已失效","data":""}
'''
def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    

    url = '%sGetMessage?ukey=%s&bid=%s&phone=%s' % (api_address,TOKEN,ITEMID,MOBILE,)
      
    response = requests.get(url=url, headers=header_dict).content.strip('"').split('|')

    key = response[0]
    value = response[1]

    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and key != "1": # 60秒内且未成功
        print(value)

        if value == "身份验证失败，请重新登录": #TOKEN错误
            login()  #再登陆
        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content.strip('"').split('|')
        key = response[0]
        value = response[1]

        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if key == "1":# 若成功
        
        text = value # change key name
        TIME = str(round(TIME2-TIME1, 1))

        d = {"time":TIME,"round":ROUND,"msg":text}
        
        return d
    else:
        print('获取短信超时，错误代码是')
        # print(response)
        print('循环数是'+ROUND)
        d = {"error":response[1],"round":ROUND}
        return d
'''
http://api.aobama.co/api/cancelRecv/?projectId=项目ID&phone=手机号码&token=登录返回token&format=json/html
http://api.wannengjm.com:6688/webapi/
'''


# this is fake release
def releasephone(ITEMID,PHONENUM):
    response = u"成功释放"

    return response



# def releasephone(ITEMID,PHONENUM):
#     url = '%sCancelRecv?&ukey=%s&bid=%s&phone=%s' % (api_address,TOKEN,ITEMID,PHONENUM)
#     response = requests.get(url=url, headers=header_dict).content.strip('"').split('|')
#     key = response[0]
#     value = response[1]
#     if key == "1":# 若成功释放
#         # MOBILE1 = response.split('|')[1]
          
#         response = u"成功释放"
#     else:
#         response = u'联系管理员，错误代号'+ value
       
#     return response