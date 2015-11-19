from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^archives/phoneusers/$', archive_phoneuser_home),
    url(r'^archives/phoneusers/view/(?P<archived_phoneuser_id>[0-9]*)$', archive_phoneuser_view),
    url(r'^archives/whitelists/$', archive_whitelist_items),
    url(r'^archives/cdrs/$', archive_cdrs_home),
    url(r'^archives/records/$', archive_records_home),
]