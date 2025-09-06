from .views import *
from django.urls import path


urlpatterns = [
    path('list/', NotificationListApiView.as_view(), name='notification-list'),
    path('update/<int:pk>/', NotificationUpdateAPIView.as_view(),
         name='notification-update'),
]
