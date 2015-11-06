from django.conf.urls import patterns

urlpatterns = [
    (r'^archives/phoneusers/$',
     phoneuser_archive),
    (r'^archives/phoneusers/(?P<archive_id>[0-9]*)$',
]