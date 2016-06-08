from django.conf.urls import url
from .views import *

urlpatterns = [
   url(r'^logs/last/$', get_last_logs),
]
