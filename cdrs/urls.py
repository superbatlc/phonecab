from django.conf.urls import patterns
from .views import *

urlpatterns = patterns('',
                   (r'^cdr/$', cdr_home),
                   (r'^cdr/ajax/filter/$', cdr_items),
                   (r'^cdr/valid/$', cdr_valid),
                   (r'^cdr/export/excel/$', cdr_export_excel),
                   )
