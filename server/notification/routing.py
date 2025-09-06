from django.urls import path
from notification.consumers import NotificationDetailConsumer

websocket_urlpatterns = [
    path('api/notification/detail/', NotificationDetailConsumer.as_asgi(),
         name='notification-detail'),

]
