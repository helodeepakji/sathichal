from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.views import loginfun
from .models import group
from home.models import sathiUser
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
                    'profile_pic': profile_pic
            }
            response.append(temp)
        if temp_array.count(temp_group.user) == 0:
            temp_array.append(temp_group.user)
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
    print(response)
    context = {"data": response}
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