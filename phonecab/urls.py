from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from phoneusers.urls import urlpatterns as phoneusers_urlpatterns
from prefs.urls import urlpatterns as prefs_urlpatterns
from cdrs.urls import urlpatterns as cdrs_urlpatterns
from records.urls import urlpatterns as records_urlpatterns

urlpatterns = patterns('',
                       (r'^$', 'phonecab.views.phonecab_login'),
                       (r'^login/$', 'phonecab.views.phonecab_login'),
                       (r'^logout/$', 'phonecab.views.phonecab_logout'),
                       (r'^phonecab/$', 'phonecab.views.phonecab_home'),
                       (r'^daynight/(?P<mode>.*)$', 'phonecab.views.phonecab_daynight'),
                       (r'^phonecab/search/$',
                        'phonecab.views.phonecab_search'),
                       (r'^phonecab/realtime/$',
                        'phonecab.views.phonecab_realtime'),
                       (r'^phonecab/user/new',
                        'phonecab.views.phonecab_user_edit'),
                       (r'^phonecab/user/edit/(?P<user_id>[0-9]*)$',
                           'phonecab.views.phonecab_user_edit'),
                       (r'^phonecab/user/save',
                        'phonecab.views.phonecab_user_save'),
                       (r'^phonecab/user/check',
                        'phonecab.views.phonecab_user_check'),
                       (r'^phonecab/user/remove/(?P<user_id>[0-9]*)',
                           'phonecab.views.phonecab_user_remove'),
                       (r'^recordings/(?P<path>.*)$', 'django.views.static.serve',
                            { 'document_root': settings.RECORDS_ROOT }),

                       (r'^admin/doc/',
                        include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += phoneusers_urlpatterns
urlpatterns += prefs_urlpatterns
urlpatterns += cdrs_urlpatterns
urlpatterns += records_urlpatterns
