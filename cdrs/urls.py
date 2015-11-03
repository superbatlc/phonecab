from django.conf.urls import patterns
from .views import *
from archives.views import archive_cdrs_home

urlpatterns = patterns('',
   (r'^cdr/$', cdr_home),
   (r'^cdr/ajax/filter/$', cdr_items),
   (r'^cdr/valid/$', cdr_valid),
   (r'^cdr/export/excel/$', cdr_export_excel),
   (r'^cdrs/archives/(?P<archive_id>[0-9]*)$', archive_cdrs_home),
)
