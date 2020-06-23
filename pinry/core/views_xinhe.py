# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse


from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView,TemplateView,View
from django_images.models import Image

from braces.views import JSONResponseMixin, LoginRequiredMixin
from django_images.models import Thumbnail

from .forms import ImageForm
from .models import Activation

import datetime
import calendar
# import yimaapi
# import xinheapi
import mayun as xinheapi


class GetSmsView_new(TemplateView):
    template_name = "getphone_new.html"
    def get_context_data(self, **kwargs):
     
        context = super(GetSmsView_new, self).get_context_data(**kwargs)
        return context

class Getphone_new(View):
    def get(self, request, app_code,phone_num='',*args, **kwargs):
        
        credit = MyProfile.objects.get(user= request.user).credit
        if credit>0:
            res = xinheapi.getphone(app_code,phone_num)
            
        else:
            res = '0|请<a href="/topup/">充值</a>'
        return HttpResponse(res)

class Releasephone_new(View):
    def get(self, request, app_code,phone_num='',*args, **kwargs):

        res = xinheapi.releasephone(app_code,phone_num)
        # res= res.decode('gbk') #解决乱码
        return HttpResponse(res)


class GetSms_new(View):
    import chardet
    def get(self, request, app_code,phonenum,*args, **kwargs):
        # phonenum = request.GET['phonenum']
        print phonenum
        res = xinheapi.getsms(phonenum,app_code)
        try:
            res = res['error']
        except:
            
            res = res['msg']
            user = request.user
            profile = MyProfile.objects.get(user= request.user)
            profile.credit -= 1           
            profile.save()

        
        return HttpResponse(res)

        # return HttpResponse(json.dumps(res), content_type='application/json')



class CreateImage(JSONResponseMixin, LoginRequiredMixin, CreateView):
    template_name = None  # JavaScript-only view
    model = Image
    form_class = ImageForm

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse('core:recent-pins'))
        return super(CreateImage, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        image = form.save()
        for size in settings.IMAGE_SIZES:
            Thumbnail.objects.get_or_create_at_size(image.pk, size)
        return self.render_json_response({
            'success': {
                'id': image.id
            }
        })

    def form_invalid(self, form):
        return self.render_json_response({'error': form.errors})

#tmp for validation to Ali union.
def root_txt(request):
    txt = 'ff322344b6bc9198061e82355f1662b2'
    return HttpResponse(response)

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

def validation(request):
    activate_code = request.GET['activate_code']
    activate_code = activate_code.strip()




    try:
        request_device_code = int(request.GET['device_code'])
    except:
        txt = 'device_code is null'
        response = 5
        return HttpResponse(response)
    try:
        a = Activation.objects.get(activate_code=activate_code)
        txt = 'code is validated'
    except:
        txt = 'wrong activate_code'
        response = 4
        return HttpResponse(response)

    try:
        owner = request.GET['owner']
        print a.owner
        print type(a.owner)
        print owner
        print type(owner)

        if a.owner.username == owner:
            pass
        else:
            response = 7
            return HttpResponse(response)
    except:
        pass

    try :
        device_code =int(a.uid)
    except:
        a.uid = request_device_code
        now = datetime.date.today()
        exp = add_months(now,1)
        a.expired_date = exp
        a.save()
        txt +='activated successfully'
        response = 2
        return HttpResponse(response)

    if device_code == request_device_code:
        txt += '& device is matched'
        response = 2
    else:
        txt += ' but device does not match'
        response = 3

    try:
        ex_date = a.expired_date
    except:
        return HttpResponse(response)


    now = datetime.date.today()
    try:
        if now <= ex_date:
            pass
        elif response == 2:
            txt += 'however expired'
            response = 6
        else:
            pass
    #exception:expired_date is null
    except:
        pass
    return HttpResponse(response)


from django.contrib.auth.decorators import login_required

@login_required
def bulk_create_validation(request):
    import random
    response = []
    for i in range(500):

        hash = random.getrandbits(128)
        hash = '%032x' % hash
        a = Activation.objects.create(activate_code = hash,owner = request.user)
        response.append(a.activate_code)



    return HttpResponse('生成成功')

from django.http import JsonResponse

from coupon import *
def get_market(request):
    jack = buyer()
    market = jack.get_market()
    return JsonResponse(market)

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from .models import Activation


class ActivationDetailView(DetailView):
    model = Activation

    template_name = 'activation_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ActivationDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# views.py


class  ActivationListView(ListView):
    model =  Activation
    template_name = 'activation_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super( ActivationListView, self).get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context
    # @login_required
    def get_queryset(self):
        
        if self.request.user.is_superuser:
            pass
        else:
            r= "not authorized"
            return r

        try:
            r = Activation.objects.filter(used=False)
        except Exception as e:
            print "HAHA"
            print e
            r= "nothing"
        return r

from django.views.generic.edit import UpdateView
from django.contrib.auth.views import redirect_to_login

class ActivationUpdateView(UpdateView):
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.owner == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(ActivationUpdateView, self).dispatch(
            request, *args, **kwargs)



    model = Activation
    fields = ['activate_code','expired_date','uid']
    template_name_suffix = '_update_form'




import logging
logger = logging.getLogger('APPNAME')
import sys,json
import urlparse
from test_ali_api import alipay
from accounts.models import MyProfile

price = {
    1:1,
    5:6,
    10:15,
    20:40
    }


def notify_validation(request):
    
    # json.dump
    # body_unicode = request.body.decode('utf-8')

    # logger.info(request.body)

    # data = '?gmt_create=2018-07-13+01%3A44%3A08&charset=utf-8&gmt_payment=2018-07-13+01%3A44%3A20&notify_time=2018-07-13+01%3A44%3A21&subject=1yuan&sign=gNeQnb45XIPBa%2FoHy4vXDc5gg0pQARs2OvHMfwZUcSH7HvgcRmsapycCWpwXNAvkVLRMwEQENk8AXFYTpNNHd5a9WTD%2BfGn3dKZJBNbEktJwO%2BqGwFD2ok63447E6JNZbUkNH3BRJig%2BWDByg1vmGWoQLaQ%2BPnkY8Kx3GvElND802CPGey5avkUrrE7chyAP99FtIetrhoV%2B8HYTfniiKIz597xs2fQbbyY0s3icNSBES0iptaVP%2FCV1tIjr0Og0mgXW8lkQgVw%2FRZL3pSGWSnaSDjazt%2BxsLsCS6pHst8j9MgvcmZCesQbutw%2B7Fi92SZUzcw2CqpJil%2B1I9jse4Q%3D%3D&buyer_id=2088802801047800&invoice_amount=1&version=1.0&notify_id=7411b27bba7e72d09599020300fc373m6d&fund_bill_list=%5B%7B%22amount%22%3A%220.01%22%2C%22fundChannel%22%3A%22ALIPAYACCOUNT%22%7D%5D&notify_type=trade_status_sync&out_trade_no=49144100908&total_amount=1&trade_status=TRADE_SUCCESS&trade_no=2018071321001004800534588101&auth_app_id=2018062460380864&receipt_amount=1&point_amount=0.00&app_id=2018062460380864&buyer_pay_amount=1&sign_type=RSA2&seller_id=2088102323393514'
    # data = request.GET['data']
    import datetime
    logger.info(datetime.datetime.now())
    logger.info('//get//')
    logger.info(request.GET)
    logger.info('//post//')
    logger.info(request.POST)
    dicted_data = request.POST
    # dicted_data = dict(urlparse.parse_qsl(urlparse.urlsplit(data).query))
    if dicted_data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        logger.info('ali trade succeed')
        amount = int(float(dicted_data["total_amount"]))
        add_value(dicted_data["out_trade_no"],amount)
        return HttpResponse('success')

    else:
        logger.info('fail')
        return HttpResponse('fail')

    # username = request.user.username    


#2018/10/13 Alipay api has expired, rewrite the notify function to add value for customer.


        
def add_value(out_trade_no,amount):
    order = Order.objects.get(uid = out_trade_no)
    order.order_status = True
    customer = order.customer
    p = MyProfile.objects.get(user= customer)
    p.credit += int(price[int(amount)])
    p.save()
    order.save()
    




        
    # pass
    # data = urlparse.parse_qs(request.body)
    # signature = data.pop('sign')
    # success = alipay.verify(data, signature)
    # try:
    #     body = json.loads(body_unicode)
    # except:
    #     print "No JSON object could be decoded"        
    # content = body['content']
    # print content
    # print body
    # signature = data.pop("sign")


    # success = alipay.verify(data, signature)

from pinry.core.models import Order
import random
import datetime
from ..users.models import User
from test_ali_api import get_alipay_url

@login_required(login_url='/accounts/signin/') 
def create_order(request,amount):
    uid = random.randint(10000000000,99999999999)
    user = User.objects.get(id=request.user.id)
    username = user.username

    try:
        Order.objects.get(uid = uid)
        
    except:
        
        order = Order(uid=uid,customer =user,amount = amount,created_time = datetime.datetime.now(),order_status= False)
        order.save()
        ali_url = get_alipay_url(amount,uid,username)
        print ali_url
        return HttpResponseRedirect(ali_url)
    else:
        return HttpResponse('failed,please try again')
    

       
class OrderListView(ListView):
    model = Order
    # context_object_name = ''
    template_name = 'order_list.html'

    def get_queryset(self):
        try:
            r = Order.objects.filter(customer=self.request.user)
        except Exception as e:
            print "HAHA"
            print e
            r= "nothing"
        return r



from django.views.generic.base import TemplateView
class TopupView(TemplateView):
    template_name = "topup.html"
    def get_context_data(self,**kwargs):
            context = super(TopupView,self).get_context_data(**kwargs)
            return context


class Home(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
     
        context = super(Home, self).get_context_data(**kwargs)
        return context

def get_error_name(code):
    error_dict = {'3005': '\xe8\xae\xa2\xe5\x8d\x95\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8', '3004': '\xe5\x8f\x91\xe9\x80\x81\xe5\xa4\xb1\xe8\xb4\xa5', '3007': '\xe4\xb8\x93\xe5\xb1\x9e\xe9\x80\x9a\xe9\x81\x93\xe6\x9c\xaa\xe5\x90\xaf\xe7\x94\xa8', '3006': '\xe4\xb8\x93\xe5\xb1\x9e\xe9\x80\x9a\xe9\x81\x93\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8', '3001': '\xe5\xb0\x9a\xe6\x9c\xaa\xe6\x94\xb6\xe5\x88\xb0\xe7\x9f\xad\xe4\xbf\xa1', '3003': '\xe6\xad\xa3\xe5\x9c\xa8\xe5\x8f\x91\xe9\x80\x81', '3002': '\xe7\xad\x89\xe5\xbe\x85\xe5\x8f\x91\xe9\x80\x81', '3008': '\xe4\xb8\x93\xe5\xb1\x9e\xe9\x80\x9a\xe9\x81\x93\xe5\xaf\x86\xe7\xa0\x81\xe4\xb8\x8e\xe9\xa1\xb9\xe7\x9b\xae\xe4\xb8\x8d\xe5\x8c\xb9\xe9\x85\x8d', '1010': '\xe5\x8f\x82\xe6\x95\xb0\xe9\x94\x99\xe8\xaf\xaf', '2010': '\xe5\x8f\xb7\xe7\xa0\x81\xe6\xad\xa3\xe5\x9c\xa8\xe4\xbd\xbf\xe7\x94\xa8\xe4\xb8\xad', '1012': '\xe7\x99\xbb\xe5\xbd\x95\xe6\x95\xb0\xe8\xbe\xbe\xe5\x88\xb0\xe4\xb8\x8a\xe9\x99\x90', '1009': '\xe8\xb4\xa6\xe6\x88\xb7\xe8\xa2\xab\xe7\xa6\x81\xe7\x94\xa8', '1008': '\xe8\xb4\xa6\xe6\x88\xb7\xe4\xbd\x99\xe9\xa2\x9d\xe4\xb8\x8d\xe8\xb6\xb3', '9003': '\xe7\xb3\xbb\xe7\xbb\x9f\xe7\xb9\x81\xe5\xbf\x99', '9002': '\xe7\xb3\xbb\xe7\xbb\x9f\xe5\xbc\x82\xe5\xb8\xb8', '9001': '\xe7\xb3\xbb\xe7\xbb\x9f\xe9\x94\x99\xe8\xaf\xaf', '1005': '\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe6\x88\x96\xe5\xaf\x86\xe7\xa0\x81\xe9\x94\x99\xe8\xaf\xaf', '1004': 'token\xe5\xa4\xb1\xe6\x95\x88', '1011': '\xe8\xb4\xa6\xe6\x88\xb7\xe5\xbe\x85\xe5\xae\xa1\xe6\xa0\xb8', '2002': '\xe9\xa1\xb9\xe7\x9b\xae\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8', '2003': '\xe9\xa1\xb9\xe7\x9b\xae\xe6\x9c\xaa\xe5\x90\xaf\xe7\x94\xa8', '2001': '\xe5\x8f\x82\xe6\x95\xb0itemid\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba', '2006': '\xe5\x8f\x82\xe6\x95\xb0mobile\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba', '2007': '\xe5\x8f\xb7\xe7\xa0\x81\xe5\xb7\xb2\xe8\xa2\xab\xe9\x87\x8a\xe6\x94\xbe', '2004': '\xe6\x9a\x82\xe6\x97\xb6\xe6\xb2\xa1\xe6\x9c\x89\xe5\x8f\xaf\xe7\x94\xa8\xe7\x9a\x84\xe5\x8f\xb7\xe7\xa0\x81', '2005': '\xe8\x8e\xb7\xe5\x8f\x96\xe5\x8f\xb7\xe7\xa0\x81\xe6\x95\xb0\xe9\x87\x8f\xe5\xb7\xb2\xe8\xbe\xbe\xe5\x88\xb0\xe4\xb8\x8a\xe9\x99\x90', '1007': '\xe5\xaf\x86\xe7\xa0\x81\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba', '1006': '\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba', '2008': '\xe5\x8f\xb7\xe7\xa0\x81\xe5\xb7\xb2\xe7\xa6\xbb\xe7\xba\xbf', '2009': '\xe5\x8f\x91\xe9\x80\x81\xe5\x86\x85\xe5\xae\xb9\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba', '1003': '\xe5\x8f\x82\xe6\x95\xb0action\xe9\x94\x99\xe8\xaf\xaf',
'1002': '\xe5\x8f\x82\xe6\x95\xb0action\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba', '1001': '\xe5\x8f\x82\xe6\x95\xb0token\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba'}
    return error_dict[str(code)]

class Beian(TemplateView):
    template_name = "beian.html"
    def get_context_data(self, **kwargs):
     
        context = super(Beian, self).get_context_data(**kwargs)
        return context




    
def use_code(request):
    code = request.POST['code']
    code = code.strip()

    try:

        a = Activation.objects.get(activate_code =code)

        if a.used == True:
            return HttpResponse('此码已被使用'+'<a href="/topup/">返回充值页面</a>')


        if a != None:
            
            a.used = True
            user = request.user
            profile = MyProfile.objects.get(user= request.user)
            profile.credit += a.value 
            profile.save()
            a.save()
            return HttpResponse(user.username + '成功充值 ' + str(a.value) +' 分<a href="/getsms_panel/">返回主界面</a>')
        
    except:
        response = '此码不正确'+'<a href="/topup/">返回充值页面</a>'
        return HttpResponse(response)

    # try:
    #     request_device_code = int(request.GET['device_code'])
    # except:
    #     txt = 'device_code is null'
    #     response = 5
    #     return HttpResponse(response)
    # try:
    #     a = Activation.objects.get(activate_code=activate_code)
    #     txt = 'code is validated'
    # except:
    #     txt = 'wrong activate_code'
    #     response = 4
    #     return HttpResponse(response)

    # try:
    #     owner = request.GET['owner']
    #     print a.owner
    #     print type(a.owner)
    #     print owner
    #     print type(owner)

    #     if a.owner.username == owner:
    #         pass
    #     else:
    #         response = 7
    #         return HttpResponse(response)
    # except:
    #     pass

    # try :
    #     device_code =int(a.uid)
    # except:
    #     a.uid = request_device_code
    #     now = datetime.date.today()
    #     exp = add_months(now,1)
    #     a.expired_date = exp
    #     a.save()
    #     txt +='activated successfully'
    #     response = 2
    #     return HttpResponse(response)

    # if device_code == request_device_code:
    #     txt += '& device is matched'
    #     response = 2
    # else:
    #     txt += ' but device does not match'
    #     response = 3

    # try:
    #     ex_date = a.expired_date
    # except:
    #     return HttpResponse(response)


    # now = datetime.date.today()
    # try:
    #     if now <= ex_date:
    #         pass
    #     elif response == 2:
    #         txt += 'however expired'
    #         response = 6
    #     else:
    #         pass
    # #exception:expired_date is null
    # except:
    #     pass
    # return HttpResponse(response)

