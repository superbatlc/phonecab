from django.conf.urls import url
from .views import *
from archives.views import archive_cdrs_home

urlpatterns = [
   url(r'^audits/$', audit_home),
   url(r'^audits/data/$', audit_items),
   #url(r'^audits/export/excel/$', audit_export_excel),
]
