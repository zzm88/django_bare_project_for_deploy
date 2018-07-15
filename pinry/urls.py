from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from pinry.core.views import notify_validation,create_order

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('pinry.core.urls', namespace='core')),
    url(r'', include('pinry.users.urls', namespace='users')),
    url(r'', include('like.urls', namespace='like')),
    #url(r'', include('tbk_picker.urls', namespace='tbk_picker')),
    #url(r'^accounts/', include('allauth.urls')),
    (r'^accounts/', include('userena.urls')),
    url(r'^ali/notify/',notify_validation),
    url(r'^create/order/(?P<amount>(\w|-)+)/$',create_order),

)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)

