from django.urls import re_path
from .views import *
from archives.views import archive_cdrs_home

urlpatterns = [
   re_path(r'^cdrs/$', cdr_home),
   re_path(r'^cdrs/ajax/filter/$', cdr_items),
   re_path(r'^cdrs/changevalid/$', cdr_change_valid),
   re_path(r'^cdrs/export/excel/$', cdr_export_excel),
   #re_path(r'^cdrs/archives/(?P<archive_id>[0-9]*)$', archive_cdrs_home),
]
