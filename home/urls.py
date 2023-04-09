from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('login', views.loginfun, name='login'),
    path('signup', views.signupfun, name='signup'),   
    path('profile', views.profile, name='profile'),   
    path('logout', views.logoutuser, name='logout'),   
]

