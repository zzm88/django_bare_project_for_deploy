# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from tastypie.api import Api

from .api import ImageResource, ThumbnailResource, PinResource, UserResource, LikeResource
from .views import CreateImage
from .views import root_txt, validation,bulk_create_validation,get_market,show_all_emails
from .views import ActivationDetailView

v1_api = Api(api_name='v1')
v1_api.register(ImageResource())
v1_api.register(ThumbnailResource())
v1_api.register(PinResource())
v1_api.register(UserResource())
v1_api.register(LikeResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls, namespace='api')),

    url(r'^pins/pin-form/$', TemplateView.as_view(template_name='core/pin_form.html'),
        name='pin-form'),
    url(r'^pins/create-image/$', CreateImage.as_view(), name='create-image'),

    url(r'^pins/tag/(?P<tag>(\w|-)+)/$', TemplateView.as_view(template_name='core/pins.html'),
        name='tag-pins'),
    url(r'^pins/user/(?P<user>(\w|-)+)/$', TemplateView.as_view(template_name='core/pins.html'),
        name='user-pins'),
    url(r'^(?P<pin>[0-9]+)/$', TemplateView.as_view(template_name='core/pins.html'),
        name='recent-pins'),

    #
    # # 原来的主页
    # url(r'^$', TemplateView.as_view(template_name='core/pins.html'),
    #     name='recent-pins'),


    url(r'^liked/$', TemplateView.as_view(template_name='core/pins.html'),
        name='liked-pins'),
    url(r'^root.txt/', view=root_txt),
    url(r'^validation/', view=validation),
    url(r'^generate_keys/', view=bulk_create_validation),
    url(r'^market/', view=get_market),
)



# urls.py:

from django.conf.urls import url

from .views import  ActivationListView,ActivationUpdateView

urlpatterns += [
    url(r'^activation/(?P<pk>[-_\w]+)/$',ActivationDetailView.as_view(), name='activation-detail'),
    url(r'^activation/edit/(?P<pk>[-_\w]+)/$',ActivationUpdateView.as_view(success_url="/"), name='activation-update'),
    url(r'^activation/$',  ActivationListView.as_view(), name='activation-list'),
    
    url(r'^mails/$',  show_all_emails, name='show_all_emails'),

]

