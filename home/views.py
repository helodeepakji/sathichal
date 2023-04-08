from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import sathiUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def index(request):
    return render(request,"index.html")

def loginfun(request):
    return render(request,"login.html")

def signupfun(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        gender = request.POST['gender']
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        addhaar = request.POST['addhaar']
        password = request.POST['password']
        confirm_password = request.POST['cpassword']
        
        # after varification of aadhaar
        
        # check if user already exists
        if sathiUser.objects.filter(username=username).exists():
            return JsonResponse({'message': 'User already exists'}, status=400)
        
        # save user to database
        newUser = sathiUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, phone=phone, aadhaarno=addhaar)
        
        # login user
        try:
            login(request, newUser)
            return JsonResponse({'message': 'User registered successfully'}, status=200)
        except:
            return JsonResponse({'message': 'Error while registering user'}, status=400)
        
    return render(request,"signup.html")