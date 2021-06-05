#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = 'f67020c10cf5c97a9c6d2e957eaa4308'


api_address = "http://api.ts.zlyjn.cn:81/api/do.php?action="
api = "api-8554-szqhbog"
password = "zzm123456"
id = "zzm123456"

'''
login()
http://api.ts.zlyjn.cn:81/api/do.php?action=loginIn&name=api-8554-szqhbog&password=zzm123456
%sloginIn&name=%s&password=%s
1|f67020c10cf5c97a9c6d2e957eaa4308

getphone()
http://api.ts.zlyjn.cn:81/api/do.php?action=getPhone&sid=2339&phone=17121655851&token=f67020c10cf5c97a9c6d2e957eaa4308
%sgetPhone&sid=%s&phone=%s&token=%s
1|17121655851|河北 未知|COM453  

getsms()
http://api.ts.zlyjn.cn:81/api/do.php?action=getMessage&sid=2339&phone=17121655851&token=f67020c10cf5c97a9c6d2e957eaa4308
%sgetMessage&sid=%s&phone=%s&token=%s
1|【探探Tantan】6544探探验证码，仅用于登录，请勿转发给他人。此验证码10分钟内有效，如果不是您本人操作，请忽略本条短信。
0|还没有接收到短信，请过3秒再试，请软件主动3秒再重新取短信内容。

release()
http://api.ts.zlyjn.cn:81/api/do.php?action=cancelRecv&sid=2339&phone=16532626435&token=f67020c10cf5c97a9c6d2e957eaa4308
%scancelRecv&sid=%s&phone=%s&token=%s
1|操作成功

'''

def login():  
    # url = ' http://api.aobama.co/api/login/?apiName=api-1309269908&password=123456&format=json
    #success response:
    #{"code":1,"msg":"success","data":"693f4780-6686-47f9-9c4a-00da4c9f906f-24537"}

    url =  "%sloginIn&name=%s&password=%s" % (api_address,api,password)    
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

    url = '%sgetPhone&sid=%s&phone=%s&token=%s' % (api_address,ITEMID,PHONENUM,TOKEN)
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
    

    url = '%sgetMessage&sid=%s&phone=%s&token=%s' % (api_address,ITEMID,MOBILE,TOKEN)
      
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
# def releasephone(ITEMID,PHONENUM):
#     response = u"成功释放"

#     return response



def releasephone(ITEMID,PHONENUM):
    url = '%scancelRecv&sid=%s&phone=%s&token=%s' % (api_address,ITEMID,PHONENUM,TOKEN)
    response = requests.get(url=url, headers=header_dict).content.strip('"').split('|')
    key = response[0]
    value = response[1]
    if key == "1":# 若成功释放
        # MOBILE1 = response.split('|')[1]
          
        response = u"成功释放"
    else:
        response = u'联系管理员，错误代号'+ value
       
    return response