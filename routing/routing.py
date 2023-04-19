from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path("ws/routing/<str:src_lat>/<str:src_lng>/<str:dest_lat>/<str:dest_lng>/", consumers.routConsumer.as_asgi()),
]