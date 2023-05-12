from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.views import loginfun
from .models import group
from home.models import sathiUser
import random
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request,"route.html")
    else :
        return redirect(loginfun)

def routing(request, src_lat, src_lng, dest_lat, dest_lng):

    source = {
        'lat' : src_lat,
        'lng' : src_lng,
    }

    destination = {
        'lat' : dest_lat,
        'lng' : dest_lng,
    }

    context = {"source":source,"destination":destination}

    return render(request,"route.html",context)


def groupget(request):
    sathi_id = request.POST.get('sathiId')
    if sathi_id:
        groups = group.objects.filter(sathi_id=sathi_id,status='P')
        response = []
        for temp_group in groups:
            if response.count(temp_group.user) == 0:
                print("temp_group.user",temp_group.user,response.count(temp_group.user))
                try:
                    profile_pic = sathiUser.objects.get(username=temp_group.user).profile_pic.url
                except:
                    profile_pic = ''
                temp = {
                        'username':temp_group.user,
                        'sathi_id':temp_group.sathi_id,
                        'profile_pic': profile_pic
                }
                response.append(temp)
                
            
    else:
        return JsonResponse({'status':'failed','message':'sathiId not found'})
    print(response)
    return JsonResponse({'response':response})


def groupupdate(request):
    sathi_id = request.POST.get('sathiId')
    print(sathi_id)
    if sathi_id:
        groups = group.objects.filter(sathi_id=sathi_id).update(status='I')
        if groups:
            # print(groups)
            response = {
                'status' : 'success',
            }
        else:
            response={
                'status' : 'failed',
            }
    return JsonResponse(response)


def startroute(request,sathi_id):
    print(sathi_id)
    groups = group.objects.filter(sathi_id=sathi_id,status='P')
    response = []
    temp_array = [] # to store the user and added_user username to avoid duplication
    # to generate the verification number for the user
    for temp_group in groups:
        if temp_group.user_verification_number == '':
            temp_group.user_verification_number = random.randint(100000,999999)
            temp_group.save()
    curr_user = {}
    for temp_group in groups:
        if temp_array.count(temp_group.user) == 0:
            temp_array.append(temp_group.user)
            try:
                profile_pic = sathiUser.objects.get(username=temp_group.user).profile_pic.url
            except:
                profile_pic = ''
            temp = {
                    'username':temp_group.user,
                    'sathi_id':temp_group.sathi_id,
                    'profile_pic': profile_pic,
            }
            # if the user is the current user
            if temp_group.user == request.user.username:
                curr_user = {
                    'username':temp_group.user,
                    'sathi_id':temp_group.sathi_id,
                    'profile_pic': profile_pic,
                    'user_verification_number':temp_group.user_verification_number
                }
            response.append(temp)
    print(response)
    context = {"current_user":curr_user,"data": response}
    print(context)
    return render(request,"startroute.html",context)

def groupname(request):
    sathi_id = request.POST.get('sathiId')
    if sathi_id:
        data = group.objects.filter(sathi_id=sathi_id).values()[0]
        data = str(data['group_name'])
        data = data.replace('_', '/')
        data = 'route/' + data[:7] + '/' + data[8:10] + '.' + data[11:13] + '/' + data[14:16] + '.' + data[17:19] + '/' + data[20:22] + '.' + data[23:25] + '/' + data[26:28] + '.' + data[29:31]
        print(data)
        response={
            'status' : 'success',
            'data' : data
        }
    else :
        response={
            'status' : 'failed',
        }
    return JsonResponse(response)



def otpverify(request):
    print(request.POST)
    sathi_id = request.POST.get('sathiId')
    user_verification_number = request.POST.get('otp')
    user = request.POST.get('username')
    response = {}
    if sathi_id and user_verification_number:
        groups = group.objects.filter(sathi_id=sathi_id,user_verification_number=user_verification_number,user=user)
        if groups:
            # print(groups)
            response = {
                'status' : 'success',
            }
        else:
            response={
                'status' : 'failed',
                'error':'Invalid OTP/user not in group'
            }
    else:
        response={
            'status' : 'failed',
            'error':'OTP or sathiId not found'
        }
    return JsonResponse(response)
