from rest_framework.generics import ListAPIView
from notification.serializers import NotificationDetailsSerializer
from notification.models.notification_model import NotificationDetails


class NotificationListApiView(ListAPIView):
    serializer_class = NotificationDetailsSerializer

    def get_queryset(self,  *args, **kwargs):
        try:
            return NotificationDetails.objects.filter(notification_is_deleted=False,
                                                      receiver=self.request.user.profile
                                                      ).order_by('-notification_created_at')

        except Exception as e:
            return self.notification_queryset.none()

    def get_serializer_context(self):
        context = {"request": self.request}
        return context
