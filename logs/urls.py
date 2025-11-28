from django.urls import re_path
from .views import *

urlpatterns = [
   re_path(r'^logs/last/$', get_last_logs),
   re_path(r'^logs/last/(?P<pk>[0-9]*)/$', get_last_logs),
]
