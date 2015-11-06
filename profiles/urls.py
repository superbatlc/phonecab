from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.profile_home),
    url(r'^users/ajax/$', views.profile_items),
    url(r'^users/(?P<pk>[0-9]+)/$', views.profile_edit),
]