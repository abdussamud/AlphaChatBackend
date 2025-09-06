from django.contrib import admin
from notification.models import NotificationImage


@admin.register(NotificationImage)
class NotificationImageAdmin(admin.ModelAdmin):
    pass
