from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^archives/phoneusers/$', archive_phoneuser_home),
    url(r'^archives/phoneusers/view/(?P<archived_phoneuser_id>[0-9]*)$', archive_phoneuser_view),
    #url(r'^archives/phoneusers/export/excel/$', archive_phoneusers_export_excel),
    url(r'^archives/whitelists/$', archive_whitelist_items),
    url(r'^archives/cdrs/$', archive_cdrs_home),
    url(r'^archives/records/$', archive_records_home),
    url(r'^archives/cdrs/export/excel/$', archive_cdrs_export_excel),
    url(r'^archives/records/export/$', archive_record_action, {'action': 'download', 'item': 'all'}),
    url(r'^archives/credits/print_recharge/(?P<archived_credit_id>[0-9]*)$', archive_credit_print_recharge),
    url(r'^archives/credits/export/(?P<archived_phoneuser_id>[0-9]*)$', archive_credit_export),
]