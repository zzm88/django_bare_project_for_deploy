# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import JsonResponse

import top
import json
from django.shortcuts import render
from django.http import HttpResponse
# 引入我们创建的表单类
from .forms import AddForm,isVaildForm
from pinry.core.models import ExpiredPin,Pin

def itemQuery(query,start_price,end_price):
    #URL等参数在base.py里修改
    req=top.api.TbkItemGetRequest()
    req.set_app_info(top.appinfo(24521510,'cdaf54fdf7f03e78cb70739c6e1e260e'))


    '''
    搜索选项
    req.cat="16,18"  #后台类目ID，用,分割，最大10个，该ID可以通过taobao.itemcats.get接口获取到
    req.itemloc="杭州"
    req.sort="tk_rate_des" #排序_des（降序），排序_asc（升序），销量（total_sales），淘客佣金比率（tk_rate）， 累计推广量（tk_total_sales），总支出佣金（tk_total_commi）
    req.is_tmall=false #天猫
    req.is_overseas=false #海涛
    req.start_price=10 #价格下限
    req.end_price=10 #价格上限
    req.start_tk_rate=123 #淘客佣金比率上限，如：1234表示12.34%
    req.end_tk_rate=123 #淘客佣金比率上限，如：1234表示12.34%
    req.platform=1#链接形式：1：PC，2：无线，默认：１
    req.page_no=123 #第几页，默认：１
    req.page_size=20 #页大小，默认20，1~100
     '''

    req.fields="num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick"

    '''
    搜索出来的产品显示哪些信息
    {u'provcity': u'\u6d59\u6c5f \u676d\u5dde',  # 地点
     u'zk_final_price': u'158.00',  # 折后价
     u'seller_id': 1676351085,  # 卖家id': 
     u'item_url': u'http://item.taobao.com/item.htm?id=553843147688',  # 链接
     u'title': u'\u6b27\u6d32\u7ad92017\u590f\u5b63\u65b0\u6b3e\u5973\u88c5\u97e9\u7248\u5bbd\u677e\u663e\u7626\u77ed\u88e4\u4e24\u4ef6\u5957\u857e\u4e1d\u65f6\u5c1a\u5957\u88c5\u5973\u6f6e',
     # 商品名称
     u'small_images': {
         u'string': [u'http://img3.tbcdn.cn/tfscom/i2/1676351085/TB2kVRRnH_0UKFjy1XaXXbKfXXa_!!1676351085.jpg',
                     u'http://img4.tbcdn.cn/tfscom/i2/1676351085/TB2DxjPumFjpuFjSspbXXXagVXa_!!1676351085.jpg',
                     u'http://img4.tbcdn.cn/tfscom/i4/1676351085/TB2MgG1yd0opuFjSZFxXXaDNVXa_!!1676351085.jpg',
                     u'http://img3.tbcdn.cn/tfscom/i1/1676351085/TB20zuAyolnpuFjSZFjXXXTaVXa_!!1676351085.jpg']},
     u'num_iid': 553843147688,  # 商品id（链接中的id）
     u'user_type': 0,
     u'volume': 10019,  # 数量
     u'nick': u'\u9192\u54e5\u5c0f\u5e97',  # 店铺名
     u'reserve_price': u'398.00',  # 原价
     u'pict_url': u'http://img3.tbcdn.cn/tfscom/i2/1676351085/TB2p1jyyb4npuFjSZFmXXXl4FXa_!!1676351085.jpg'}
    '''
    req.q=query.encode('utf-8')
    req.start_price=start_price #价格下限
    req.end_price=end_price #价格上限


    # req.format = "json"

    try:
        resp= req.getResponse()
        print '1'
    except Exception,e:
        print(e)

    items = resp["tbk_item_get_response"]["results"]["n_tbk_item"]
    for i in items:
        print i

    return items #return a list

    """b

    Args:


    Returns:

    """


    '''d
    #turn  resp into json
    resp = json.dumps(resp)
    print type(resp)
    '''

    '''
    #输出html文件
    import os.path
    save_path = 'C:/Users/user/OneDrive/taobao-sdk-PYTHON-auto_1486971200958-20170709/'
    
    name_of_file = raw_input("enter a name")
    
    completeName = os.path.join(save_path, name_of_file+".html")
    
    Html_file= open(completeName, "w")
    
    Html_file.write(resp)
    Html_file.close()
    '''
# Create your views here.


def search(request):
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            query = form.cleaned_data['query']
            start_price = form.cleaned_data['start_price']
            end_price = form.cleaned_data['end_price']
            items = itemQuery(query, start_price, end_price)
            return render_to_response('search_result.html', {"items":itemQuery(query,start_price,end_price)})

    else:  # 当正常访问时
        form = AddForm()
    return render(request, 'search_form.html', {'form': form})


def getFvrList(request=None):
    # -*- coding: utf-8 -*-
    import top.api

    req = top.api.TbkUatmFavoritesGetRequest()
    req.set_app_info(top.appinfo(24521510, 'cdaf54fdf7f03e78cb70739c6e1e260e'))

    req.page_no = 1
    req.page_size = 20
    req.fields = "favorites_title,favorites_id,type"
    req.type = 1
    try:
        resp = req.getResponse()

        favourites = resp['tbk_uatm_favorites_get_response']['results']['tbk_favorites']
        pretty(resp)
    except Exception, e:
        print(e)
    if not request:
        return favourites
    return render(request, 'favourites.html', {"items":favourites})

    # return render_to_response('favourites.html', {"items":favourites})

def getFvrItem(request=None,fav_id=None):
    # -*- coding: utf-8 -*-
    import top.api

    req = top.api.TbkUatmFavoritesItemGetRequest()
    req.set_app_info(top.appinfo(24521510, 'cdaf54fdf7f03e78cb70739c6e1e260e'))

    req.platform = 1
    req.page_size = 20
    req.adzone_id = 122118293
    req.unid = "3456"
    req.favorites_id = fav_id
    req.page_no = 1
    req.fields = "num_iid,click_url,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick,shop_title,zk_final_price_wap,event_start_time,event_end_time,tk_rate,status,type"
    try:
        resp = req.getResponse()

        pretty(resp)
        print resp
        favourites = resp['tbk_uatm_favorites_item_get_response']['results']['uatm_tbk_item']
        #hiding pins that have been chosen before.
        delete_existed_pin(favourites)

    except Exception, e:
        print(e)

    if request == None:
        return favourites
    return render(request,'favourite_items.html', {"items":favourites})

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)


def get_taokouling(request):
    url = request.POST['tbk_url']
    description = request.POST.get('description')
    print url
    print type(url)
    url = url.encode('utf-8')
    description = description.encode('utf-8')

    import top.api
    req = top.api.WirelessShareTpwdCreateRequest()
    req.set_app_info(top.appinfo(24521510, 'cdaf54fdf7f03e78cb70739c6e1e260e'))
    req.tpwd_param = "{'url':'" + url + "','text':'" + description + "'}"
    try:
        resp = req.getResponse()
        tkl = resp['wireless_share_tpwd_create_response']
    except Exception, e:
        print(e)
    return JsonResponse(tkl)

#view images of items. data come from attribute of link.
def view_images(request):
    print request.POST
    print request
    img_urls = request.POST['img_urls']
    print type(img_urls)
    print img_urls
    img_urls = img_urls.encode()
    img_urls = img_urls.strip('][').split(',')
    print img_urls
    print type(img_urls)
    def clean(string):
        string = string.strip("u' ")
        return string
    img_urls = map(clean,img_urls)
    foo = {'img_urls':img_urls}
    return JsonResponse(foo)

# don't have the permission to access the api.
def is_vaild(request):
    if request.method == 'POST':  # 当提交表单时

        form = isVaildForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            num_iid = form.cleaned_data['num_iid']
            return render_to_response('search_result.html', {"items":top_isValid(num_iid)})

    else:  # 当正常访问时
        form = isVaildForm()
    return render(request, 'search_form.html', {'form': form})

# don't have the permission to access this top
#
# api.
def top_isValid(num_iid):
    import top.api

    req = top.api.TbkRebateAuthGetRequest()
    req.set_app_info(top.appinfo(24521510,'cdaf54fdf7f03e78cb70739c6e1e260e'))
    req.fields = "param,rebate"
    req.params = num_iid
    req.type = 1
    try:
        resp = req.getResponse()
        print(resp)
    except Exception, e:
        print(e)


# find out expired pins and create records in database
def set_expired_to_database(request):
    fav_list=get_fav_list()
    for fav_id in fav_list:
        items = getFvrItem(fav_id = fav_id)
        for item in items:
            try:
                item['click_url']
            except:
                ExpiredPin.objects.get_or_create(num_iid = item['num_iid'])
    return render_to_response('panel.html',{'msg':'success'})

def get_fav_list():
    resp = getFvrList()
    fav_list = []
    for fav in resp:
        fav_list.append(fav['favorites_id'])
    #do sth to resp, so that you get a fav_id list.
    return fav_list

#delete expired pin according to records in database
def delete_expired_pin(request):
    expired_pin= get_expired_pin()
    expired_pin.delete()
    return render_to_response('panel.html',{'msg':'deleted'})

    # ExpiredPin.objects.all.remove() # empty the data of expired pin

def get_expired_pin():
    expired_pin= Pin.objects.filter(num_iid__in= list_of_expired())
    return expired_pin #which is a query_set

def list_of_expired():
    list_of_expired = ExpiredPin.objects.all()
    id_list_of_expired=[]
    for exp_pin in list_of_expired:
        id_list_of_expired.append(exp_pin.num_iid)
    return id_list_of_expired


from django.views.generic.base import TemplateView

class CommonView(TemplateView):
    template_name = "panel.html"

    def get_context_data(self, **kwargs):
        context = super(CommonView, self).get_context_data(**kwargs)
        return context


def delete_existed_pin(pins):

    existed_pins = Pin.objects.all()
    for pin in pins:
        try:
            Pin.objects.get(num_iid = pin['num_iid'])
            pins.remove(pin)
        except:
            pass

