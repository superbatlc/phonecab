from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^records/$', record_home),
    re_path(r'^records/ajax/filter/$', record_items),
    re_path(r'^records/remove/$', record_action, {'action': 'remove', 'item': 'all'}),
    re_path(r'^records/remove/(?P<record_id>[0-9]*)$', record_action, {'action': 'remove', 'item': 'single'}),
    re_path(r'^records/show_warning/$', record_show_warning),
    re_path(r'^records/export/$', record_action, {'action': 'download', 'item': 'all'}),
    re_path(r'^records/export/(?P<record_id>[0-9]*)$', record_action, {'action': 'download', 'item': 'single'}),
]
