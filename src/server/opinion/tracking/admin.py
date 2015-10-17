from django.contrib import admin
from tracking.models import VisitorTracked, BannedIP, UntrackedUserAgent

admin.site.register(VisitorTracked)
admin.site.register(BannedIP)
admin.site.register(UntrackedUserAgent)