from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from phoneusers.urls import urlpatterns as phoneusers_urlpatterns
from prefs.urls import urlpatterns as prefs_urlpatterns
from cdrs.urls import urlpatterns as cdrs_urlpatterns
from records.urls import urlpatterns as records_urlpatterns
from profiles.urls import urlpatterns as profiles_urlpatterns

urlpatterns = [
    url(r'^$', 'phonecab.views.phonecab_login'),
    url(r'^login/$', 'phonecab.views.phonecab_login'),
    url(r'^logout/$', 'phonecab.views.phonecab_logout'),
    url(r'^phonecab/$', 'phonecab.views.phonecab_home'),
    url(r'^daynight/(?P<mode>.*)$', 'phonecab.views.phonecab_daynight'),
    url(r'^phonecab/search/$',
    'phonecab.views.phonecab_search'),
    url(r'^phonecab/realtime/$',
    'phonecab.views.phonecab_realtime'),
    url(r'^recordings/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': settings.RECORDS_ROOT }),

    url(r'^admin/doc/',
    include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += phoneusers_urlpatterns
urlpatterns += prefs_urlpatterns
urlpatterns += cdrs_urlpatterns
urlpatterns += records_urlpatterns
urlpatterns += profiles_urlpatterns
