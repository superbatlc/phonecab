from django.contrib import admin
from .models import *

admin.site.register(ArchivedPhoneUser)
admin.site.register(ArchivedWhitelist)
admin.site.register(ArchivedCredit)
admin.site.register(ArchivedDetail)
admin.site.register(ArchivedRecord)

