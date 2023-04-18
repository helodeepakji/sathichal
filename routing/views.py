from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.views import loginfun
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request,"route.html")
    else :
        return redirect(loginfun)
 
def rout(request,lat,long):
    # return JsonResponse({'lat': lat,'long':long}, status=400)
    return render(request,"route.html")