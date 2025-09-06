from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification(notification_object):
    """
    params:
        notification_object
    return:
        send notification to user
    description:
        send notification to user 
    """
    channel_layer = get_channel_layer()
    group_name = 'notification_details'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification.message',
            'message': notification_object
        }
    )


async def notification_message(self, event):
    await self.send_json(event['message'])
