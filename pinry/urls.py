from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from pinry.core.views import notify_validation,create_order,OrderListView,GetSmsView,Getphone,GetSms,TopupView,Beian,Jui,Home,use_code
from pinry.core.views_xinhe import GetSmsView_new,Getphone_new,GetSms_new,Releasephone_new
admin.autodiscover()
from userena import views as userena_views

from django.contrib.auth.decorators import login_required
    

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('pinry.core.urls', namespace='core')),
    url(r'', include('pinry.users.urls', namespace='users')),
    url(r'', include('like.urls', namespace='like')),
    # url(r'^$',HomePageView.as_view(), name='homepage')

    #url(r'', include('tbk_picker.urls', namespace='tbk_picker')),
    #url(r'^accounts/', include('allauth.urls')),
    (r'^accounts/', include('userena.urls')),

    url(r'^ali/notify/',notify_validation),
    url(r'^order/create/(?P<amount>(\w|-)+)/$',create_order),

    url(r'^order/list$',OrderListView.as_view(),name = 'order_list'),
    
    url(r'^getsms_panel/$',login_required(GetSmsView.as_view()) , name='getsmsview'),
    url(r'^getphone/(?P<app_code>(\w|-)+)/$', Getphone.as_view(), name='getphone'),
    url(r'^getphone/(?P<app_code>(\w|-)+)/(?P<phone_num>(\w|-)+)/$', Getphone.as_view(), name='getphone'),
    url(r'^getsms/(?P<app_code>(\w|-)+)/(?P<phonenum>(\w|-)+)/$', GetSms.as_view(), name='getsms'),
    url(r'^topup/use_code/$', use_code),

    url(r'^topup/$', login_required(TopupView.as_view()), name='topup'),

    #url(r'^$', Beian.as_view(), name='beian'),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^jui/$', Jui.as_view(), name='jui'),
    url(r'^bookstore/', include('bookstore.urls')),
    
    # (r'^bookstore/', include('bookstore.urls')),


    url(r'^getsms_panel_new/$',login_required(GetSmsView_new.as_view()) , name='getsmsview_new'),
    url(r'^getphone_new/(?P<app_code>(\w|-)+)/$', Getphone_new.as_view(), name='getphone_new'),
    url(r'^getphone_new/(?P<app_code>(\w|-)+)/(?P<phone_num>(\w|-)+)/$', Getphone_new.as_view(), name='getphone_new'),
    url(r'^release_new/(?P<app_code>(\w|-)+)/(?P<phone_num>(\w|-)+)/$', Releasephone_new.as_view(), name='release_new'),
    url(r'^getsms_new/(?P<app_code>(\w|-)+)/(?P<phonenum>(\w|-)+)/$', GetSms_new.as_view(), name='getsms_new'),
    

    
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)






