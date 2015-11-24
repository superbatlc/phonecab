from django.conf.urls import url
from .views import *

urlpatterns = [
   url(r'^audits/$', audit_home),
   url(r'^audits/data/$', audit_items),
   #url(r'^audits/export/excel/$', audit_export_excel),
]
