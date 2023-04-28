from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.views import loginfun
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
    response = {
        'username': {
            'username' : 'username',
            'sathi_id' : 'sathi_id',
            'profile_pic' : 'profile_pic'
        },
        'username': {
            'username' : 'username',
            'sathi_id' : 'sathi_id',
            'profile_pic' : 'profile_pic'
        }
    }
    return JsonResponse(response)


def groupupdate(request):
    response = {}
    return JsonResponse(response)