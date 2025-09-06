from rest_framework import serializers
from notification.models import NotificationImage


class NotificationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationImage
        fields = ('id', 'image')
