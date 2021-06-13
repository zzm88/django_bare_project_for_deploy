#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.test import TestCase
import requests
import time
import json
from .models import Token

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = 'bb7bdaaaec034ed1986f1c2620afb848'


api_address = "http://150.242.99.60:8888/api/"
api = ""
password = "123456"
id = "zzmdianjingyun2"

'''
1.format
0|登陆成功|token=bb7bdaaaec034ed1986f1c2620afb848

2.需要转码
content.decode('gb2312').encode('utf-8')


login()
http://150.242.99.60:8888/api/login?username=zzmdianjingyun2&password=123456
%slogin?username=%s&password=%s
0|登陆成功|token=bb7bdaaaec034ed1986f1c2620afb848


getphone()
http://150.242.99.60:8888/api/getjmphone?yysxz=0&token=bb7bdaaaec034ed1986f1c2620afb848&qylx=0&xmid=31&qygjz=&yys=0&qyxz=0&author=zzmdianjingyun2
%sgetjmphone?yysxz=0&token=%s&qylx=0&xmid=%s&qygjz=&yys=0&qyxz=0&author=zzmdianjingyun2
0|17131634484|浙江|宁波

getsms()
http://150.242.99.60:8888/api/jmgetMessage?token=bb7bdaaaec034ed1986f1c2620afb848&xmid=31&phone=17131634484
%sjmgetMessage?token=%s&xmid=%s&phone=%s
0|已完成|31|17050782621|【探探Tantan】2267探探验证码，仅用于登录，请勿转发给他人。此验证码10分钟内有效，如果不是您本人操作，请忽略本条短信。|2267

release()
http://150.242.99.60:8888/api/jmSpecified?token=bb7bdaaaec034ed1986f1c2620afb848&xmid=31&phone=17131634484
%sjmSpecified?token=%s&xmid=%s&phone=%s
0|释放成功

'''




def login():  
    '''
    login()
    http://150.242.99.60:8888/api/login?username=zzmdianjingyun2&password=123456
    %slogin?username=%s&password=%s
    0|登陆成功|token=bb7bdaaaec034ed1986f1c2620afb848

    '''
    url =  "%slogin?username=%s&password=%s" % (api_address,id,password)    
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312')
    response = requests.get(url=url, headers=header_dict).content.strip('"')

    global TOKEN 
    if response.split('|')[0] == "0": #登陆成功
        TOKEN = response.split('|')[2]
    else:
        pass
    




'''http://api.aobama.co/api/getPhone/?projectId=66658&card=虚拟&phone=&pre=&loop=0&token=693f4780-6686-47f9-9c4a-00da4c9f906f-24537&operate=zzm88aobaoma&format=json

{"code":1,"msg":"操作成功","data":"16573800365"}
'''


def getphone(ITEMID,PHONENUM=''):
    '''
    http://150.242.99.60:8888/api/getjmphone?yysxz=0&token=bb7bdaaaec034ed1986f1c2620afb848&qylx=0&xmid=31&qygjz=&yys=0&qyxz=0&author=zzmdianjingyun2
    %sgetjmphone?yysxz=0&token=%s&qylx=0&xmid=%s&qygjz=&yys=0&qyxz=0&author=zzmdianjingyun2
    0|17131634484|浙江|宁波'''

    url = '%sgetjmphone?yysxz=0&token=%s&qylx=0&xmid=%s&qygjz=&yys=0&qyxz=0&author=zzmdianjingyun2' % (api_address,TOKEN,ITEMID)
    # response = requests.get(url=url, headers=header_dict).content.decode('utf-8').encode('gb2312') 
    response = requests.get(url=url, headers=header_dict).content.strip('"').split("|")
    key= response[0]
    value = response[1]

    if  key == "1"  :#TOKEN错误，重新登录
        login()#登录
        response = getphone(ITEMID,PHONENUM) #再次获取手机
        # response = json.loads(response)['reasonCode']
    elif key == "0":#取号成功
       return value
    else:#取号失败
        response = value
        return u'联系管理员%s' % (response)

def getsms(MOBILE,ITEMID):    
    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
   
    WAIT = 60 # 接受短信时长60s
    
    '''getsms()
    http://150.242.99.60:8888/api/jmgetMessage?token=bb7bdaaaec034ed1986f1c2620afb848&xmid=31&phone=17131634484
    %sjmgetMessage?token=%s&xmid=%s&phone=%s
    0|已完成|31|17050782621|【探探Tantan】2267探探验证码，仅用于登录，请勿转发给他人。此验证码10分钟内有效，如果不是您本人操作，请忽略本条短信。|2267

    '''


    url = '%sjmgetMessage?token=%s&xmid=%s&phone=%s' % (api_address,TOKEN,ITEMID,MOBILE)
      
    response = requests.get(url=url, headers=header_dict).content.strip('"').split('|')

    key = response[0]
    value = response[1]

    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1


    while (TIME2-TIME1) < WAIT and key == "1": # 60秒内且未成功
        print(value)

        # if value == "账号已被冻结": #TOKEN错误
        #     login()  #再登陆
        
        time.sleep(5)
        response = requests.get(url=url, headers=header_dict).content.decode('gb2312').encode('utf-8').strip('"').split('|')
        # response = requests.get(url=url, headers=header_dict).content.strip('"').split('|')
        key = response[0]
        
        value = response[1]


        TIME2 = time.time()
        ROUND = ROUND+1
        print "try"+str(ROUND)
        
    ROUND = str(ROUND)
    if key == "0":# 若成功

        value = response[4]#此行比较特别，只有在电竞云出现，value在成功的时候是第四个，失败时没有四个会出错
        
        
        text = value 
        TIME = str(round(TIME2-TIME1, 1))

        d = {"time":TIME,"round":ROUND,"msg":text}
        
        return d
    else:
        print('获取短信超时，错误代码是')
        # print(response)
        print('循环数是'+ROUND)
        d = {"error":response[1],"round":ROUND}
        return d



# this is fake release
# def releasephone(ITEMID,PHONENUM):
#     response = u"成功释放"

#     return response



def releasephone(ITEMID,PHONENUM):
    url = '%sjmSpecified?token=%s&xmid=%s&phone=%s' % (api_address,TOKEN,ITEMID,PHONENUM)
    response = requests.get(url=url, headers=header_dict).content.decode('gb2312').encode('utf-8').strip('"').split('|')
    key = response[0]
    value = response[1]
    if key == "0":# 若成功释放
        # MOBILE1 = response.split('|')[1]
          
        response = u"成功释放"
    else:
        response = u'联系管理员，错误代号'+ value
       
    return response


def transform_jumble(jumble):
    
    str = jumble
    b = repr(str)
    tidy_words = unicode(eval(b),"gbk")
    return tidy_words