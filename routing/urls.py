from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.route, name='rout'),
    path('routing/<str:src_lat>/<str:src_lng>/<str:dest_lat>/<str:dest_lng>', views.routing, name='routing'),
]

