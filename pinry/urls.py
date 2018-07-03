from django.conf import settings
from django.conf.urls import  include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
]



# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += patterns('', url(r'^media/(?P<path>.*)$',
#         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)

