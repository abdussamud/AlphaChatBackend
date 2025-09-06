from chat.models import RoomMessage
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from notification.models import NotificationDetails
from notification.serializers import NotificationDetailsSerializer


@database_sync_to_async
def create_notification_object(
    sender,
    notification_type,
    receiver=None,
    message=None,
    plain_text=None,
    description=None,
    heading=None,


):
    _message = message
    _receiver = receiver
    if _message:
        _message = get_object_or_404(RoomMessage, id=message)
        if _message.room.partner.user == sender:
            _receiver = _message.room.owner.user
        if _message.room.partner.user != sender:
            _receiver = _message.room.partner.user
        _message = _message

    notification_object = NotificationDetails.objects.create(
        sender=sender.profile,
        receiver=_receiver.profile,
        message=_message,
        heading=heading,
        plain_text=plain_text,
        description=description,
        notification_type=notification_type,


    )
    get_notification_object = NotificationDetails.objects.all().last()
    notification_object_serializer = NotificationDetailsSerializer(
        get_notification_object)
    return notification_object_serializer.data
