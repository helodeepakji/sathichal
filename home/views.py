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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # authenticate user
        user = authenticate(request, username=username, password=password)
        
        if not sathiUser.objects.filter(username=username).exists():
            return JsonResponse({'message': 'User does not exist'}, status=400)
        
        # if user exists
        if user is not None:
            # login user
            login(request, user)
            return JsonResponse({'message': 'User logged in successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
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
        
        # check if password and confirm password match
        if password == confirm_password:
            # password saved in database is hashed
            db_password = make_password(password)
        else:
            return JsonResponse({'message': 'Passwords do not match'}, status=400)
        
        # after varification of aadhaar
        
        # check if user already exists
        if sathiUser.objects.filter(username=username).exists():
            return JsonResponse({'message': 'User already exists'}, status=400)
        
        # save user to database
        newUser = sathiUser.objects.create_user(username=username, email=email, password=db_password, first_name=first_name, last_name=last_name, phone=phone, aadhaarno=addhaar)
        
        # login user
        try:
            login(request, newUser)
            return JsonResponse({'message': 'User registered successfully'}, status=200)
        except:
            return JsonResponse({'message': 'Error while registering user'}, status=400)
        
    return render(request,"signup.html")