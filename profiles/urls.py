from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^profiles/$', profile_home),
    re_path(r'^profiles/data/$', profile_items),
    re_path(r'^profiles/edit/$', profile_edit),
    re_path(r'^profiles/save/$', profile_save),
    re_path(r'^profiles/check/$', profile_check_username),
    re_path(r'^profiles/changestatus/$', profile_change_status),
]