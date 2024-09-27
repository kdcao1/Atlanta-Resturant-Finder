from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from .models import Guest
from .forms import ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import base64


def home(request):
    if not request.user.is_authenticated:
        return redirect('/foodFinder/login/')
    else:
        return render(request, "foodFinder/home.html", context=None)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Registration was successful!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'foodFinder/register.html')




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

        # Handle the cropped image data if provided
        cropped_image_data = request.POST.get('cropped_image_data', None)

        if form.is_valid():
            if cropped_image_data:
                # Logic to handle the cropped image
                from django.core.files.base import ContentFile
                import base64

                # Decode the cropped image data
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{guest.user.username}_profile.{ext}')

                # Save the cropped image to the guest profile
                guest.profile_picture = data
                guest.save()

            form.save()
            return redirect('settings')
    else:
        form = ProfileForm(instance=guest)

    context = {
        'form': form,
        'guest': guest,  # Include guest to show current profile picture
    }
    return render(request, 'foodFinder/settings.html', context)
