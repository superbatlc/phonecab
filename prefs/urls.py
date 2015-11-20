from django.conf.urls import patterns
from .views import *

urlpatterns = patterns('',
    (r'^prefs/edit/$', prefs_edit),
    (r'^prefs/save/$', prefs_save),
                       )
