from django.shortcuts import redirect, render
# import requests
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
        
        # if user does not exist
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
        full_name = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        gender = request.POST['gender']
        dob = request.POST['dob']
        first_name = full_name.split(" ")[0]
        
        # if user gives full name
        if len(full_name.split(" ")) > 1:
            last_name = full_name.split(" ")[-1]
        else:
            # if user gives only first name
            last_name = ""
        addhaar = ""
        password = request.POST['password']
        confirm_password = request.POST['cpassword']
        
        # check if password and confirm password match
        if password != confirm_password or password == "" or confirm_password == "":
            return JsonResponse({'message': 'Passwords do not match / Invalid password values'}, status=400)
        

        # after varification of phone number
        
        # check if user already exists
        if sathiUser.objects.filter(username=username).exists() or sathiUser.objects.filter(email=email).exists() or sathiUser.objects.filter(phone=phone).exists():
            return JsonResponse({'message': 'User already exists'}, status=400)
        
        
        # save user to database
        newUser = sathiUser.objects.create(username=username, email=email,gender=gender, password=make_password(password), first_name=first_name, last_name=last_name, phone=phone, aadhaarno=addhaar, dob=dob)
        newUser.save()
        
        
        # login user
        try:
            login(request, newUser)
            return JsonResponse({'message': 'User registered successfully'}, status=200)
        except:
            return JsonResponse({'message': 'Error while registering user'}, status=400)
        
    return render(request,"signup.html")


def logoutuser(request):
    logout(request)
    return redirect(loginfun)


def profile(request):
    # if request.user.is_authenticated:
        data = sathiUser.objects.filter(username="helodeepakji").values()
        context = {"data":data[0]}
        return render(request,"profile.html",context)
    # else:
    #     return redirect(loginfun)
