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

def bulk_create_validation(request):
    import random
    response = []
    for i in range(10):

        hash = random.getrandbits(128)
        hash = '%032x' % hash
        a = Activation.objects.create(activate_code = hash)
        response.append(a.activate_code)


    return HttpResponse(response)
