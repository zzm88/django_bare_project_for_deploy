from django.conf.urls import patterns,url ,include
urlpatterns = patterns('',
    url(r'^search/$', 'tbk_picker.views.search', name='search'),
    url(r'^isvalid/$', 'tbk_picker.views.is_vaild', name='isvalid'),
    url(r'^favourites/$', 'tbk_picker.views.getFvrList', name='favourites'),
    url(r'^favourites/(\d+)/$', 'tbk_picker.views.getFvrItem', name='fav_items'),
    url(r'^gettkl/$', 'tbk_picker.views.get_taokouling', name='get_tkl'),
    url(r'^view_images/$', 'tbk_picker.views.view_images', name='view_images'),

    # url(r'^tbk_items/$',view=ItemList),
)