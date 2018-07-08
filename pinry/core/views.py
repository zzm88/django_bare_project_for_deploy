# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse


from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django_images.models import Image

from braces.views import JSONResponseMixin, LoginRequiredMixin
from django_images.models import Thumbnail

from .forms import ImageForm
from .models import Activation

import datetime
import calendar

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
    for i in range(10):

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
    def get_queryset(self):
        try:
            r = Activation.objects.filter(owner=self.request.user)
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

from test_ali_api import alipay
def notify_validation(request):
    data = request.GET['data']
    signature = data.pop("sign")
    success = alipay.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
        print("ali trade succeed")