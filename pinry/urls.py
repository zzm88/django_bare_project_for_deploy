from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from pinry.core.views import notify_validation,create_order,OrderListView,GetSmsView,Getphone,GetSms,TopupView
admin.autodiscover()
from userena import views as userena_views

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
    url(r'^order/list$',OrderListView.as_view()),
    
    url(r'^getsms_panel/$', GetSmsView.as_view(), name='getsmsview'),
    url(r'^getphone/$', Getphone.as_view(), name='getphone'),
    url(r'^getsms/$', GetSms.as_view(), name='getsms'),
    url(r'^topup/$', TopupView.as_view(), name='topup'),
 



)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)

