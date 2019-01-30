from django.conf.urls import url,include,patterns
from rest_framework import routers
from bookstore import views
from rest_framework.urlpatterns import format_suffix_patterns

print(views)
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'entry', views.EntryViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [

    url('', include(router.urls)),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
  
]


urlpatterns += [

    url(r'^entryurl/(?P<url>[0-9a-f-]+)/$', views.entry_detail),

]

# urlpatterns = format_suffix_patterns(urlpatterns)

from bookstore.views import EntryDetailView,TopupView
from django.contrib.auth.decorators import login_required
from bookstore.views import EntryListView,OrderListView,Home
from bookstore.views import bookstore_signup,bookstore_signin,bookstore_signout


urlpatterns += [
    url(r'^view/entry/(?P<url>[0-9a-f-]+)/$', EntryDetailView.as_view(), name='entry-detail'),
    url(r'^buy/(?P<pk>\w+)/$', views.buy,name='bookstore-buy'),
    url(r'^topup/$', login_required(TopupView.as_view(),login_url='/bookstore/accounts/signin'),name='bookstore-topup'),
    url(r'^entrylist$', EntryListView.as_view(), name='entry-list'),
    url(r'^orderlist$', OrderListView.as_view(), name='bookstore-order-list'),
    url(r'^home/$', Home.as_view(), name='bookstore-home'),
    url(r'^accounts/signup', bookstore_signup, name='bookstore-signup'),
    url(r'^accounts/signin', bookstore_signin, name='bookstore-signin'),
    url(r'^accounts/signout', bookstore_signout, name='bookstore-signout'),


]
