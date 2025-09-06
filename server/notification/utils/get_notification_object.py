from django.db.models import When,Case
from channels.db import database_sync_to_async
from notification.models import NotificationDetails

@database_sync_to_async
def get_notification_object(object_id):
    notification_object= NotificationDetails.objects.get(id=object_id)
    return notification_object