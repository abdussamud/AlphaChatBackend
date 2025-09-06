from django.contrib import admin
from notification.models import NotificationDetails


@admin.register(NotificationDetails)
class NotificationAdmin(admin.ModelAdmin):
    pass