from rest_framework import serializers
from notification.models import NotificationImage
from notification.models import NotificationDetails


class NotificationDetailsSerializer(serializers.ModelSerializer):
    """
    serializer for notification details
    """

    notification_image = serializers.SerializerMethodField()
    sender_image = serializers.ImageField(
        source='sender.image', read_only=True)
    sender_name = serializers.CharField(
        source='sender.user.username', read_only=True)
    sender_last_name = serializers.CharField(
        source='sender.last_name', read_only=True)
    sender_first_name = serializers.CharField(
        source='sender.first_name', read_only=True)
    is_user_online = serializers.BooleanField(
        source='sender.is_online', read_only=True)
    unread_notification_count = serializers.SerializerMethodField()

    class Meta:
        model = NotificationDetails
        fields = [
            'id',
            'sender',
            'heading',
            'message',
            'receiver',
            'receiver',
            'plain_text',
            'sender_name',
            'description',
            'sender_image',
            'is_user_online',
            'sender_last_name',
            'sender_first_name',
            'notification_type',
            'notification_image',
            'notification_is_read',
            'notification_created_at',
            'notification_is_deleted',
            'unread_notification_count',
            ]

    def get_notification_image(self, obj):
        return NotificationImage.objects.last().image.url

    def get_unread_notification_count(self, obj):
        return NotificationDetails.objects.filter(notification_is_read=False, receiver=obj.receiver).count()
