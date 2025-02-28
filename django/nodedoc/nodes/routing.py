from django.urls import re_path
from .consumers import NodeConsumer

websocket_urlpatterns = [
    re_path(r'ws/nodes/$', NodeConsumer.as_asgi()),
]