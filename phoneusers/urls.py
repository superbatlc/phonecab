from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^phoneusers/$', phoneuser_home),
    re_path(r'^phoneusers/new/$', phoneuser_edit),
    re_path(r'^phoneusers/view/(?P<phoneuser_id>[0-9]*)$', phoneuser_view),
    re_path(r'^phoneusers/edit/$', phoneuser_edit),
    re_path(r'^phoneusers/save/$', phoneuser_save),
    #re_path(r'^phoneusers/export/(?P<pincode>[0-9]*)$', phoneuser_export),
    re_path(r'^phoneusers/name/(?P<pincode>[0-9]*)$', phoneuser_name),
    re_path(r'^phoneusers/data/(?P<phoneuser_id>[0-9]*)$', phoneuser_data),
    re_path(r'^phoneusers/realtime/info/$', phoneuser_realtime_info),
    #re_path(r'^phoneusers/enable/(?P<phoneuser_id>[0-9]*)$', phoneuser_enable),
    #re_path(r'^phoneusers/disable/(?P<phoneuser_id>[0-9]*)$', phoneuser_disable),
    re_path(r'^phoneusers/changestatus/$', phoneuser_change_status),
    re_path(r'^phoneusers/check/pincode/$', phoneuser_check_pincode),
    re_path(r'^phoneusers/check/whitelist/$', phoneuser_check_whitelist),
    re_path(r'^phoneusers/archive/$', phoneuser_archive),
    re_path(r'^phoneusers/export/excel/$', phoneuser_export_excel),

    re_path(r'^whitelists/$', whitelist_items),
    re_path(r'^whitelists/edit/$', whitelist_edit),
    re_path(r'^whitelists/save/$', whitelist_save),
    re_path(r'^whitelists/remove/$', whitelist_remove),
    re_path(r'^whitelists/changestatus/$', whitelist_change_status),
    re_path(r'^whitelists/changeordinary/$', whitelist_change_ordinary),
    re_path(r'^whitelists/changeadditional/$', whitelist_change_additional),
    re_path(r'^whitelists/checkextra/$', whitelist_check_extra),
    #re_path(r'^whitelist/edit/(?P<whitelist_id>[0-9]*)$',
    # whitelist_edit),
    re_path(r'^credits/$', credit_items),
    re_path(r'^credits/new/$', credit_new),
    re_path(r'^credits/save/$', credit_save),
    re_path(r'^credits/print_recharge/(?P<credit_id>[0-9]*)$', credit_print_recharge),
    re_path(r'^credits/export/(?P<phoneuser_id>[0-9]*)$', credit_export),

]
