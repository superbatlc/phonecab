from django.contrib import admin
from .models import PhoneUser, Whitelist, Credit

admin.site.register(PhoneUser)
admin.site.register(Whitelist)
admin.site.register(Credit)
