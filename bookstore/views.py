# -*- coding: utf-8 -*-

import sys

from django.contrib.auth.models import Group, User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from userena import views as userena_views

from bookstore.serializers import (EntrySerializer, GroupSerializer,
                                   UserSerializer)
from models import Entry
from pinry.core.models import Order

reload(sys)
sys.setdefaultencoding('utf8')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    search_fields = ( 'url')


#output a json entry detail
@api_view(['GET'])
def entry_detail(request, url):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        entry = Entry.objects.get(url=url)
    except Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EntrySerializer(entry)
        return Response(serializer.data)




class EntryDetailView(DetailView):
    
    model = Entry
    


    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        try:
            all_ownership = self.request.user.entry_set.all()
            target_entry = Entry.objects.get(url = self.kwargs['url'])
            result = target_entry in all_ownership
            context['ownership'] = result
            get_general_context(self,context)
        except:
            pass
        return context
   
    def get_object(self):
        return get_object_or_404(Entry, url=self.kwargs['url'])

'''
detail_view documentation:
https://docs.djangoproject.com/en/1.8/ref/class-based-views/generic-display/#detailview
 
'''


# purchase entry
from django.contrib.auth.decorators import login_required

@login_required(login_url='/bookstore/accounts/signin')
def buy(request,pk):
    buyer = request.user
    target_entry = Entry.objects.get(pk = pk)

    if request.user.my_profile.credit>0:
        request.user.my_profile.credit-=1
        request.user.my_profile.save()
        request.user.entry_set.add(target_entry)  
        html = "<html><body>购买成功 <a href = '/bookstore/view/entry/%s'>返回</a></body></html>" % target_entry.url
        return HttpResponse(html)


    else:
        html = "<html><body>请充值 <a href = '/bookstore/view/entry/%s'>返回</a></body></html>" % target_entry.url
        return HttpResponse(html)

 

class TopupView(TemplateView):
    template_name = "bookstore/topup.html"
    def get_context_data(self,**kwargs):
            context = super(TopupView,self).get_context_data(**kwargs)
            get_general_context(self,context)
            
            return context




class EntryListView(ListView):
    model = Entry
    # template_name = "TEMPLATE_NAME"
    
    def get_context_data(self, **kwargs):
        context = super(EntryListView,self).get_context_data(**kwargs)
        get_general_context(self,context)

        return context
    

class OrderListView(ListView):
    model = Order
    # context_object_name = ''
    template_name = 'bookstore/order_list.html'
    
    def get_queryset(self):
        try:
            r = Order.objects.filter(customer=self.request.user)
        except Exception as e:
            print "HAHA"
            print e
            r= "nothing"
        return r

    def get_context_data(self, **kwargs):
         
        context = super(OrderListView, self).get_context_data(**kwargs)
        get_general_context(self,context)

        return context

class Home(TemplateView):
    template_name = "bookstore/home.html"
    def get_context_data(self, **kwargs):
     
        context = super(Home, self).get_context_data(**kwargs)
        get_general_context(self,context)

        return context


def get_general_context(view,context):

    try:
        context['left_credit'] = view.request.user.my_profile.credit
    except AttributeError:
        pass


from django.http import HttpResponseRedirect

def bookstore_signup(request):
    # do stuff before userena signup view is called
    extra_context=dict()
    extra_context['override_base'] = 'bookstore/bookstore-base.html'
    # call the original view
    response = userena_views.signup(request,extra_context=extra_context)

    # do stuff after userena signup view is done
    if request.method=='POST':
        try:
            if response.url:
                response = HttpResponseRedirect('/bookstore/topup/')
        except:
            pass    # do stuff after userena signup view is done
    # return the response
    # return the response
    return response

def bookstore_signin(request):
    # do stuff before userena signup view is called
    extra_context=dict()
    extra_context['override_base'] = 'bookstore/bookstore-base.html'
    # call the original view
    from userena.utils import signin_redirect
    response = userena_views.signin(request,extra_context=extra_context)
    if request.method=='POST':
        try:
            if response.url:
                response = HttpResponseRedirect('/bookstore/home/')
        except:
            pass

    # do stuff after userena signup view is done
    # return the response
    return response


def bookstore_signout(request):
    # do stuff before userena signup view is called
    extra_context=dict()
    extra_context['override_base'] = 'bookstore/bookstore-base.html'
    # call the original view
    response = userena_views.signout(request,extra_context=extra_context)


    # do stuff after userena signup view is done

    # return the response
    return response

