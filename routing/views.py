from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.views import loginfun
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request,"route.html")
    else :
        return redirect(loginfun)
 
def rout(request):
    return JsonResponse({'message': 'Working'}, status=400)