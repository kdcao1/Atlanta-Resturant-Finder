from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "foodFinder/home.html", context=None)


def login(request):
    return HttpResponse("Hello, world. You're at the login.")

def favorites(request):
    return HttpResponse("Hello, world. You're at the favorites.")

def settings(request):
    return HttpResponse("Hello, world. You're at the settings.")