from django.conf.urls import patterns,url ,include
from views import CommonView

urlpatterns = patterns('',
    url(r'^search/$', 'tbk_picker.views.search', name='search'),
    url(r'^isvalid/$', 'tbk_picker.views.is_vaild', name='isvalid'),
    url(r'^favourites/$', 'tbk_picker.views.getFvrList', name='favourites'),
    url(r'^favourites/(\d+)/$', 'tbk_picker.views.getFvrItem', name='fav_items'),
    url(r'^gettkl/$', 'tbk_picker.views.get_taokouling', name='get_tkl'),
    url(r'^getclickurl/$', 'tbk_picker.views.get_clickurl', name='get_clickurl'),
    url(r'^view_images/$', 'tbk_picker.views.view_images', name='view_images'),
    url(r'^delete/expiredpins$', 'tbk_picker.views.delete_expired_pin', name='delete_expired_pin'),
    url(r'^create/expiredpins$', 'tbk_picker.views.set_expired_to_database', name='set_expired_to_database'),
    url(r'^panel$', CommonView.as_view(), name='panel '),

    # url(r'^tbk_items/$',view=ItemList),
)