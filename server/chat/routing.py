from .consumers import (
    ChatUpdateConsumers,
    OnlineStatusConsumer,
    DashboardChatConsumer,
    UserOnlineStatusConsumer,
    GroupActivityAsyncConsumer,

)
from django.urls import path


websocket_urlpatterns = [

    path('api/group/activity/chat/',
         GroupActivityAsyncConsumer.as_asgi()),
    path('api/dashboard/chat/', DashboardChatConsumer.as_asgi()),
    path('api/online/status/', OnlineStatusConsumer.as_asgi()),
    path('api/chat/update/', ChatUpdateConsumers.as_asgi()),
    path('api/user/online/status/', UserOnlineStatusConsumer.as_asgi()),
]
