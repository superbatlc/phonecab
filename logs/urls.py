from django.conf.urls import url
from .views import *

urlpatterns = [
   url(r'^logs/last/$', get_last_logs),
   url(r'^logs/last/(?P<pk>[0-9]*)/$', get_last_logs),
]
