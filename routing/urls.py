from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('routing/<str:src_lat>/<str:src_lng>/<str:dest_lat>/<str:dest_lng>', views.routing, name='routing'),
    path('groups/get',views.groupget, name='groupget'),
    path('groups/update/',views.groupupdate, name='groupupdate'),
    path('groups/name/',views.groupname, name='groupname'),
    path('groups/otpverify/',views.otpverify, name='otpverify'),
    path('startroute/<str:sathi_id>',views.startroute, name='startroute'),
]

