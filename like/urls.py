from django.conf.urls import patterns,url ,include
from like.views import *
urlpatterns = patterns('',
    url(r'^pins/like/(?P<pin_id>(\w|-)+)/$',view=like),
    url(r'^pins/unlike/(?P<pin_id>(\w|-)+)/$',view=unlike),
    url(r'^pins/voted/(?P<pin_id>(\w|-)+)/$',view=is_voted),
    url(r'^pins/voted_pins/$',view=voted_pins),


)