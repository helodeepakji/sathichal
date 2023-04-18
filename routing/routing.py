from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/routing/(?P<src_lat>\w+)/(?P<src_lng>\w+)/(?P<dst_lat>\w+)/(?P<dst_lng>\w+)/$", consumers.routConsumer.as_asgi()),
]