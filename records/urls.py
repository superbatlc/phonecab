from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^records/$', record_home),
    url(r'^records/ajax/filter/$', record_items),
    url(r'^records/remove/$', record_action, {'action': 'remove', 'item': 'all'}),
    url(r'^records/remove/(?P<record_id>[0-9]*)$', record_action, {'action': 'remove', 'item': 'single'}),
    url(r'^records/export/$', record_action, {'action': 'download', 'item': 'all'}),
    url(r'^records/export/(?P<record_id>[0-9]*)$', record_action, {'action': 'download', 'item': 'single'}),
]
