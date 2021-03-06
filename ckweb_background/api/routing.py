#django的路由叫urls.py
#对于channels有新的路由文件
from django.urls import re_path

from . import consumers  #等同于views.py 稍后创建

websocket_urlpatterns = [
    re_path(r'ws/api/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]