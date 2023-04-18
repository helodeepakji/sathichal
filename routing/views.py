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
    print(src_lat, src_lng, dest_lat, dest_lng)
    return JsonResponse({'src_lat': src_lat,'src_lng': src_lng,'dest_lat': dest_lat,'dest_lng': dest_lng,}, status=400)