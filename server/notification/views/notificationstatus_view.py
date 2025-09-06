from notification.models import NotificationDetails
from notification.serializers import NotificationDetailsSerializer
from rest_framework.generics import UpdateAPIView
from django.db.models import When,Case

class NotificationUpdateAPIView(UpdateAPIView):
    queryset = NotificationDetails.objects.all()
    serializer_class = NotificationDetailsSerializer

    def perform_update(self, serializer):
        is_delete_notification=self.request.data['is_delete']
        if is_delete_notification:
            serializer.save(notification_is_deleted=True)
        serializer.save(notification_is_read=True)