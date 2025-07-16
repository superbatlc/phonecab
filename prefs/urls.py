from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^prefs/edit/$', prefs_edit),
    re_path(r'^prefs/save/$', prefs_save)
]
