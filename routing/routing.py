from django.urls import path

from . import consumers
from . import startroute

websocket_urlpatterns = [
    path("ws/routing/<str:src_lat>/<str:src_lng>/<str:dest_lat>/<str:dest_lng>/", consumers.routConsumer.as_asgi()),
    path("ws/routing/<str:sath_id>/", startroute.sathiRoute.as_asgi()),
]