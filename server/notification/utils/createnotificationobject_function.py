from django.db.models import When, Case
from notification.models import NotificationDetails
from notification.serializers import NotificationDetailsSerializer


def create_notification_object_apis(
    sender,
    receiver,
    notification_type,
    plain_text=None,
    description=None,
    heading=None,





):
    """
    params:
        sender,
        heading,
        plain_text,
        gig,message,
        description,
        notification_type,
    return:
        serialized notification object data

    description:
        create notification object for send notification to user
    """
    notification_object = NotificationDetails.objects.create(
        heading=heading,
        sender=sender.profile,
        receiver=receiver.profile,
        plain_text=plain_text,
        description=description,
        notification_type=notification_type,

    )

    get_notification_object = NotificationDetails.objects.last()
    # serialized notification object data
    notification_object_serializer = NotificationDetailsSerializer(
        get_notification_object)
    return notification_object_serializer.data
