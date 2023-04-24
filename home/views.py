from django.shortcuts import redirect, render
# import requests
from django.http import JsonResponse
from .models import sathiUser, Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .util import otp_handler

# for testing

userOtp = otp_handler()

def ajaxfile(request):
    phone = request.POST['phone']
    print(phone)
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_ACCOUNT_AUTH_TOKEN)
    print(userOtp)
    message = client.messages.create(
        body = f"Your OTP is {userOtp}",
        from_ = settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
    response = {
        'status': "successfull Otp Send"
    }
    return JsonResponse(response)


# Create your views here.

def index(request):
    return render(request,"index.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        
        contact = Contact(name=name, email=email, phone=phone, question=message)
        contact.save()
        # send email to admin
        # putting my own mail as receiver for testing
        subject = "New message from sathichal.com"
        email_message = f"Name: {name}\nemail: {email}\nphone: {phone}\nmessage: {message}" 
        email_from = settings.EMAIL_HOST_USER
        reciepent_list = ['helodeepakji@gmail.com']
        send_mail(subject, email_message, email_from, reciepent_list, fail_silently=False)
        return JsonResponse({'message': 'Message sent successfully'}, status=200)
    return render(request,"contact.html")


def routing(request):
    if request.user.is_authenticated:
        return render(request,"routing.html")
    else :
        return redirect(loginfun)
       


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
            return redirect(index)
        else:
            return redirect(loginfun)
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
        otp = request.POST['otp']

        # print(otp)
        global userOtp
        print("userOtp",userOtp)
        
        if int(otp) != userOtp:
            return JsonResponse({'message': 'Invalid OTP'}, status=400)
        else :
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
            
            # check if user already exists
            if sathiUser.objects.filter(username=username).exists() or sathiUser.objects.filter(email=email).exists() or sathiUser.objects.filter(phone=phone).exists():
                return JsonResponse({'message': 'User already exists'}, status=400)
            
            # save user to database
            newUser = sathiUser.objects.create(username=username, email=email,gender=gender, password=make_password(password), first_name=first_name, last_name=last_name, phone=phone, aadhaarno=addhaar, dob=dob)
            newUser.save()
            
            # make the otp none after user is registered
            # userOtp = None
            
            # login user
            try:
                login(request, newUser)
                return redirect(index)
            except:
                return redirect(signupfun)
            
    return render(request,"signup.html")


def logoutuser(request):
    logout(request)
    return redirect(loginfun)


def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            data = sathiUser.objects.get(username=request.user)
            context = {"data":data}
            return render(request,"profile.html",context)
        else:
            return redirect(loginfun)
    if request.method == 'POST':
        name = request.POST['name']
        first_name = name.split(" ")[0]
        if len(name.split(" ")) > 1:
            last_name = name.split(" ")[-1]
        else:
            last_name = ""
        dob = request.POST['age']
        email = request.POST['email']
        phone = request.POST['phone']
        gov_id = request.POST['aadhar']
        city = request.POST['city']
        state = request.POST['state']
        profile = request.FILES.get('profile',None)
        sathiuser = sathiUser.objects.get(username=request.user)
        if sathiuser:
            sathiuser.first_name = first_name
            sathiuser.last_name = last_name
            sathiuser.dob = dob
            sathiuser.email = email
            sathiuser.aadhaarno = gov_id
            sathiuser.city = city
            sathiuser.state = state
            sathiuser.profile_pic = profile
            sathiuser.save()
            # if sathiuser.phone != phone:
            #     #verify phone number
            
            # else:
            #     sathiuser.phone = phone
            return redirect(profile)
