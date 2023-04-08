from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def loginfun(request):
    return render(request,"login.html")

def signupfun(request):
    return render(request,"signup.html")