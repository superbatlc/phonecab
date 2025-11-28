from django.urls import re_path
from .views import *

urlpatterns = [
   re_path(r'^audits/$', audit_home),
   re_path(r'^audits/data/$', audit_items),
   #re_path(r'^audits/export/excel/$', audit_export_excel),
]
