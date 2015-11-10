from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^profiles/$', profile_home),
    url(r'^profiles/data/$', profile_items),
    url(r'^profiles/edit/$', profile_edit),
    url(r'^profiles/save/$', profile_save),
    url(r'^profiles/remove/$', profile_remove),
    url(r'^profiles/check/$', profile_check_username),
]