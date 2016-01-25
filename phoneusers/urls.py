from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^phoneusers/$', phoneuser_home),
    url(r'^phoneusers/new/$', phoneuser_edit),
    url(r'^phoneusers/view/(?P<phoneuser_id>[0-9]*)$', phoneuser_view),
    url(r'^phoneusers/edit/$', phoneuser_edit),
    url(r'^phoneusers/save/$', phoneuser_save),
    #url(r'^phoneusers/export/(?P<pincode>[0-9]*)$', phoneuser_export),
    url(r'^phoneusers/name/(?P<pincode>[0-9]*)$', phoneuser_name),
    url(r'^phoneusers/data/(?P<phoneuser_id>[0-9]*)$', phoneuser_data),
    url(r'^phoneusers/realtime/info/$', phoneuser_realtime_info),
    #url(r'^phoneusers/enable/(?P<phoneuser_id>[0-9]*)$', phoneuser_enable),
    #url(r'^phoneusers/disable/(?P<phoneuser_id>[0-9]*)$', phoneuser_disable),
    url(r'^phoneusers/changestatus/$', phoneuser_change_status),
    url(r'^phoneusers/check/$', phoneuser_check_pincode),
    url(r'^phoneusers/archive/$', phoneuser_archive),

    url(r'^whitelists/$', whitelist_items),
    url(r'^whitelists/edit/$', whitelist_edit),
    url(r'^whitelists/save/$', whitelist_save),
    url(r'^whitelists/remove/$', whitelist_remove),
    url(r'^whitelists/changestatus/$', whitelist_change_status),
    url(r'^whitelists/changeordinary/$', whitelist_change_ordinary),
    url(r'^whitelists/checkextra/$', whitelist_check_extra),                   
    #url(r'^whitelist/edit/(?P<whitelist_id>[0-9]*)$',
    # whitelist_edit),
    url(r'^credits/$', credit_items),
    url(r'^credits/new/$', credit_new),
    url(r'^credits/save/$', credit_save),
    url(r'^credits/print_recharge/(?P<credit_id>[0-9]*)$', credit_print_recharge),
    url(r'^credits/export/(?P<phoneuser_id>[0-9]*)$', credit_export),
    
]
