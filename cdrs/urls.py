from django.conf.urls import patterns
from .views import *
from archives.views import archive_cdrs_home

urlpatterns = patterns('',
   (r'^cdrs/$', cdr_home),
   (r'^cdrs/ajax/filter/$', cdr_items),
   (r'^cdrs/valid/$', cdr_valid),
   (r'^cdrs/export/excel/$', cdr_export_excel),
   (r'^cdrs/archives/(?P<archive_id>[0-9]*)$', archive_cdrs_home),
)
