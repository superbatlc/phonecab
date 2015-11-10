from django.conf.urls import url
from .views import *
from archives.views import archive_cdrs_home

urlpatterns = [
   url(r'^cdrs/$', cdr_home),
   url(r'^cdrs/ajax/filter/$', cdr_items),
   url(r'^cdrs/valid/$', cdr_valid),
   url(r'^cdrs/export/excel/$', cdr_export_excel),
   url(r'^cdrs/archives/(?P<archive_id>[0-9]*)$', archive_cdrs_home),
]
