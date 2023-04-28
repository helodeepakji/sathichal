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
            if response.count(temp_group.added_by_user) == 0:
                print("temp_group.added_by_user",temp_group.added_by_user,response.count(temp_group.added_by_user))
                try:
                    profile_pic = sathiUser.objects.get(username=temp_group.added_by_user).profile_pic.url
                except:
                    profile_pic = ''
                temp = {
                    temp_group.added_by_user :{
                        'username':temp_group.added_by_user,
                        'sathi_id':temp_group.sathi_id,
                        'profile_pic': profile_pic
                    }
                }
                response.append(temp)
            if response.count(temp_group.added_user) == 0:
                # temp_user = sathiUser.objects.get(username=temp_group.added_user)
                print("temp_group.added_user",temp_group.added_user,response.count(temp_group.added_user))
                try:
                    profile_pic = sathiUser.objects.get(username=temp_group.added_user).profile_pic.url
                except:
                    profile_pic = ''
                temp = {
                temp_group.added_user:{
                    'username':temp_group.added_user,
                    'sathi_id':temp_group.sathi_id,
                    'profile_pic': profile_pic
                    }
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