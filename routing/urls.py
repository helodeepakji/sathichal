from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:lat>/<str:long>', views.rout, name='rout'),
]

