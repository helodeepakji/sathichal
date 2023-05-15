from django.shortcuts import redirect, render
# import requests
from django.http import JsonResponse
from .models import sathiUser, Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from routing.models import group, chat, feedback
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .util import otp_handler, cal_feedback

# for testing

userOtp = otp_handler()

def ajaxfile(request):
    phone = request.POST['phone']
    # print(phone)
    
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

def order(request):
    username = request.user.username
    sathi_ids = group.objects.filter(user = username, status = 'C') # change it to C for production
    groups = []
    for sathi_id in sathi_ids:
        temp_groups = group.objects.filter(sathi_id = sathi_id.sathi_id, status = 'C') # change it to C for production
        split_group_name = sathi_id.group_name.split('_')
        src_lat = split_group_name[1]+'.'+split_group_name[2]
        src_long = split_group_name[3]+'.'+split_group_name[4]
        dest_lat = split_group_name[5]+'.'+split_group_name[6]
        dest_long = split_group_name[7]+'.'+split_group_name[8]
        user_list = []
        for temp_group in temp_groups:
            user_name = temp_group.user
            user_list.append(user_name)
        temp = {
            'sathi_id': sathi_id.sathi_id,
            'is_feedback': sathi_id.is_feedback,
            'users': user_list,
            'location':{
                'src_lat': src_lat,
                'src_long': src_long,
                'dest_lat': dest_lat,
                'dest_long': dest_long,
            },
            'date': sathi_id.date,
        }
        groups.append(temp)
    print(groups)
    
    context = {'groups': groups}
    return render(request,"order.html",context)

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
        sathiuser = sathiUser.objects.get(username=request.user)
        dob = request.POST['age']
        if dob == "":
            dob = sathiuser.dob
        email = request.POST['email']
        phone = request.POST['phone']
        gov_id = request.POST['aadhar']
        city = request.POST['city']
        state = request.POST['state']
        profile = request.FILES.get('profile',None)
        gender = request.POST['gender']
        # update user details
        if sathiuser:
            sathiUser.objects.filter(username=request.user).update(first_name=first_name,last_name=last_name,email=email,phone=phone,dob=dob,aadhaarno=gov_id,city=city,state=state,profile_pic=profile,gender=gender)
            
            # if sathiuser.phone != phone:
            #     #verify phone number
            
            # else:
            #     sathiuser.phone = phone
        return render(request,"profile.html",{"data":sathiuser})



def feedback_handler(request,sathi_id):
    username = request.user.username
    print(sathi_id)
    print(request.method)
    # get method return the userdetails (name,username,profile,group_location,sathi_id,date,time) and self given_by feedback
    if request.method == "GET":
        # temp_feedback = feedback.objects.filter(sathi_id=sathi_id,feedback_given_by=username)
        temp_group = group.objects.filter(sathi_id=sathi_id,status='C')
        
        temp_location = temp_group[0].group_name.split("_")
        src_lat = temp_location[1]+"."+temp_location[2]
        src_long = temp_location[3]+"."+temp_location[4]
        dest_lat = temp_location[5]+"."+temp_location[6]
        dest_long = temp_location[7]+"."+temp_location[8]
        # print(group_location)
        context = []
        if temp_group:
            for sathi_user in temp_group:
                error=""
                temp_profile_pic = sathiUser.objects.get(username=sathi_user.user).profile_pic
                # if object exists
                try:
                    temp_feedback = feedback.objects.get(user=sathi_user.user,sathi_id=sathi_id,feedback_given_by=username)
                # if object does not exist 
                except:
                    temp_feedback = None
                    error = "No feedback given"
                if temp_feedback != None:
                    if temp_feedback.feedback:
                        comments = temp_feedback.feedback
                    else:
                        comments = ""
                    if temp_feedback.rating:
                        rating = (temp_feedback.rating/5)*100
                    else:
                        rating = 0
                else:
                    comments = ""
                    rating = 0
                
                # list of comments and feedback of user
                
                if temp_profile_pic:
                    profile_pic = temp_profile_pic.url
                else:
                    profile_pic = ""
                if sathiUser.objects.get(username=sathi_user.user).username != username:
                    user = {
                        'first_name':sathiUser.objects.get(username=sathi_user.user).first_name,
                        'last_name':sathiUser.objects.get(username=sathi_user.user).last_name,
                        'username':sathiUser.objects.get(username=sathi_user.user).username,
                        'profile_pic': profile_pic,
                        'src_lat':src_lat,
                        'src_long':src_long,
                        'dest_lat':dest_lat,
                        'dest_long':dest_long,
                        'sathi_id':sathi_id,
                        'is_feedback': sathi_user.is_feedback,
                        'rating': rating,
                        'comment': comments,
                        'date': sathi_user.date,
                        'time' : sathi_user.time,
                        'error':error
                    }
                    context.append(user)
        else:
            context = {'error':'invalid sathi id'}
        return render(request,"feedback.html",{'data':context})
    # post method add feedback if no existing feedback other update feedback and group table is_feedback trure
    if request.mehod == "POST":
        current_feedback = request.POST['feedback']
        
        sathiuser = sathiUser.objects.get(username=username)
        
        groups = group.objects.get(sathi_id=sathi_id,status='C')
        groups.is_feedback = True
        groups.save()
        temp_feedback1 = feedback.objects.create(feedback_given_by=sathiuser.username,user = sathiuser.username,feedback=current_feedback)
        temp_feedback1.save()
        return redirect(index)

    return render(request,"feedback.html")