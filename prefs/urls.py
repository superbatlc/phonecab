from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^prefs/edit/$', prefs_edit),
    url(r'^prefs/save/$', prefs_save)
]
