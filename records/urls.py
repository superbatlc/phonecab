from django.conf.urls import patterns
from .views import *

urlpatterns = patterns('',
                       (r'^records/$', record_home),
                       (r'^records/ajax/filter/$', record_items),
                       (r'^records/remove/$', record_action,
                        {'action': 'remove', 'item': 'all'}),
                       (r'^records/remove/(?P<record_id>[0-9]*)$',
                           record_action, {'action': 'remove', 'item': 'single'}),
                       (r'^records/export/$', record_action,
                           {'action': 'download', 'item': 'all'}),
                       (r'^records/export/(?P<record_id>[0-9]*)$',
                           record_action, {'action': 'download', 'item': 'all'}),
                       #(r'^records/test_zip/$', test_zip),
                       )
