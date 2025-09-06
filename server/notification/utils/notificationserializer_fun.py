from channels.db import database_sync_to_async
from notification.serializers import NotificationDetailsSerializer


@database_sync_to_async
def get_notification(notification_object):
    serializer = NotificationDetailsSerializer(notification_object)
    return serializer.data
