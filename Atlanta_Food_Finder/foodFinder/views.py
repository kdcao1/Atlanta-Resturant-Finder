from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from .models import Guest, Restaurant
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *

def home(request):
    return render(request, "foodFinder/home.html", context=None)

def logins(request):
    login_error = False
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            print("Bad Login")
            login_error = True
        else:
            # Log in the user and redirect to the home page upon successful login
            print("Good Login")
            login(request, user)
            return redirect('/foodFinder')
    context = {
        "login_error": login_error
    }
    return render(request, "foodFinder/login.html", context)

def favorites(request):
    return render(request, "foodFinder/favorites.html", context=None)

def settings(request):
    return render(request, "foodFinder/settings.html", context=None)

@login_required
def settings(request):
    guest = Guest.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = ProfileForm(instance=guest)

    context = {
        'form': form,
    }
    return render(request, 'foodFinder/settings.html', context)