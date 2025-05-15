"""
General Url pattern
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
admin.autodiscover()

from phoneusers.urls import urlpatterns as phoneusers_urlpatterns
from prefs.urls import urlpatterns as prefs_urlpatterns
from cdrs.urls import urlpatterns as cdrs_urlpatterns
from records.urls import urlpatterns as records_urlpatterns
from profiles.urls import urlpatterns as profiles_urlpatterns
from audits.urls import urlpatterns as audits_urlpatterns
from archives.urls import urlpatterns as archives_urlpatterns
from tools.urls import urlpatterns as tools_urlpatterns
from logs.urls import urlpatterns as logs_urlpatterns

from phonecab.views import *

urlpatterns = [
    url(r'^$', phonecab_login),
    url(r'^login/$', phonecab_login),
    url(r'^logout/$', phonecab_logout),
    url(r'^phonecab/$', phonecab_realtime),
    url(r'^nightmode/$', phonecab_get_nightmode),
    url(r'^nightmode/(?P<mode>.*)$', phonecab_set_nightmode),

    url(r'^recordings/(?P<path>.*)$', serve,
        {'document_root': settings.RECORDS_ROOT}),

    url(r'^admin/doc/',
        include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += phoneusers_urlpatterns
urlpatterns += prefs_urlpatterns
urlpatterns += cdrs_urlpatterns
urlpatterns += records_urlpatterns
urlpatterns += profiles_urlpatterns
urlpatterns += audits_urlpatterns
urlpatterns += archives_urlpatterns
urlpatterns += tools_urlpatterns
urlpatterns += logs_urlpatterns
