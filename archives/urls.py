from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^archives/phoneusers/$', archive_phoneuser_home),
    re_path(r'^archives/phoneusers/view/(?P<archived_phoneuser_id>[0-9]*)$', archive_phoneuser_view),
    #re_path(r'^archives/phoneusers/export/excel/$', archive_phoneusers_export_excel),
    re_path(r'^archives/whitelists/$', archive_whitelist_items),
    re_path(r'^archives/cdrs/$', archive_cdrs_home),
    re_path(r'^archives/records/$', archive_records_home),
    re_path(r'^archives/cdrs/export/excel/$', archive_cdrs_export_excel),
    re_path(r'^archives/records/export/$', archive_record_action, {'action': 'download', 'item': 'all'}),
    re_path(r'^archives/credits/print_recharge/(?P<archived_credit_id>[0-9]*)$', archive_credit_print_recharge),
    re_path(r'^archives/credits/export/(?P<archived_phoneuser_id>[0-9]*)$', archive_credit_export),
]