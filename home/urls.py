from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('routing', views.routing, name='routing'),
    path('login', views.loginfun, name='login'),
    path('signup', views.signupfun, name='signup'),  
    path('contact', views.contact, name='contact'),   
    path('profile', views.profile, name='profile'),   
    path('logout', views.logoutuser, name='logout'),
    path('ajaxfile', views.ajaxfile, name='ajaxfile'),   
]

