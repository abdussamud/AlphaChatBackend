from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer
)
from notification.utils import get_notification, get_notification_object


class NotificationDetailConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.notification_group_name = 'notification_details'

        # Join room group
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, content):

        user = self.scope['user']
        notification_object = await get_notification_object(object_id=2)
        notification_serialized_data = await get_notification(notification_object=notification_object)
        await self.channel_layer.group_send(
            self.notification_group_name,
            {
                'type': 'notification.message',
                'message': notification_serialized_data
            }
        )

    # Receive message from room group
    async def notification_message(self, event):
        await self.send_json(event['message'])
