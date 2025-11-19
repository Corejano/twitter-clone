from django.urls import re_path
from apps.chat.consumers import ChatConsumer, NotificationsConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>[0-9a-f-]+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationsConsumer.as_asgi()),
]
