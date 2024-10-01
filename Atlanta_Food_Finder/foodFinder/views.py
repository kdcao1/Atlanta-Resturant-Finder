from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import ProfileForm, Favorite
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from .models import UserProfile
import os
from dotenv import load_dotenv
load_dotenv()

port = os.getenv('PORT')

def home(request):
    if not request.user.is_authenticated:
        return redirect('/foodFinder/login/')

    guest = Guest.objects.get(user=request.user)

    if request.POST.get('action') == 'favorite':
        print('loved')
        placeId = request.POST.get('placeId')
        form = Favorite(request.POST)
        if form.is_valid():
            restaurant = Restaurant.objects.get_or_create(
                placeId=placeId,
            )
            restaurant = Restaurant.objects.get(placeId=placeId)
            guest.favorite_restaurants.add(restaurant)
            guest.save()

    if request.POST.get('action') == 'unfavorite':
        print('unloved')
        placeId = request.POST.get('placeId')
        form = Favorite(request.POST)
        if form.is_valid():
            restaurant = Restaurant.objects.get(placeId=placeId)
            guest.favorite_restaurants.remove(restaurant)
            guest.save()

    context = {
        'lovedPlaces': guest.favorite_restaurants.all(),
        'apiKey': os.getenv('GMAPS_API_KEY'),
        'port': port,
    }
    return render(request, "foodFinder/home.html", context)


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

                # Creates the associated Guest object for the new user
                guest = Guest.objects.create(user=user, location='Unknown')
                guest.save()

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
        user = authenticate(request, username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            print("Bad Login")
            login_error = True
        else:
            # Log in the user and redirect to the home page upon successful login
            print("Good Login")
            login(request, user)

            try:
                user_profile = UserProfile.objects.get(user=user)
                return redirect('/foodFinder')  # Redirect to the desired URL with UserProfile
            except UserProfile.DoesNotExist:
                # Handle case where UserProfile does not exist
                # Redirect to a different page or create a UserProfile here if needed
                return redirect('/create-profile')  # Example redirect to profile creation page

    context = {
        "login_error": login_error
    }
    return render(request, "foodFinder/login.html", context)

def favorites(request):
    if not request.user.is_authenticated:
        return redirect('/foodFinder/login/')

    guest = Guest.objects.get(user=request.user)

    if request.POST.get('action') == 'unfavorite':
        placeId = request.POST.get('placeId')
        form = Favorite(request.POST)
        if form.is_valid():
            restaurant = Restaurant.objects.get(placeId=placeId)
            guest.favorite_restaurants.remove(restaurant)
            guest.save()

    context = {
        'lovedPlaces': guest.favorite_restaurants.all(),
        'apiKey': os.getenv('GMAPS_API_KEY'),
        'port': port,
    }

    return render(request, "foodFinder/favorites.html", context)


@require_POST
def favorite_restaurant(request, restaurant_id):
    if request.user.is_authenticated:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        if restaurant in request.user.guest.favorite_restaurants.all():
            request.user.guest.favorite_restaurants.remove(restaurant)
            is_favorited = False
        else:
            request.user.guest.favorite_restaurants.add(restaurant)
            is_favorited = True
        return JsonResponse({'is_favorited': is_favorited})
    return JsonResponse({'error': 'User not authenticated'}, status=403)


def settings(request):
    if not request.user.is_authenticated:
        return redirect('/foodFinder/login/')

    guest = Guest.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    can_edit = False

    if request.method == "POST":
        if request.POST.get('action') == 'logout':
            logout(request)
            print('Logged Out')
            return redirect('/foodFinder/login')

        if request.POST.get('action') == 'edit':
            can_edit = True

        if request.POST.get('action') == 'cancel':
            return redirect('/foodFinder/settings')

        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        cropped_image_data = request.POST.get('cropped_image_data', None)

        if form.is_valid() and not request.POST.get('action') == 'edit':

            print("submitted")
            # Handle profile picture cropping
            if cropped_image_data:
                from django.core.files.base import ContentFile
                import base64

                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{guest.user.username}_profile.{ext}')

                guest.profile_picture = data

            # Save guest profile and user details
            guest.user.email = request.POST.get('email', guest.user.email)
            guest.user.username = request.POST.get('username', guest.user.username)
            guest.location = request.POST.get('location', guest.location)
            guest.first_name = request.POST.get('first_name',guest.first_name)
            guest.last_name = request.POST.get('last_name', guest.last_name)

            # Handle profile picture upload if provided
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                user_profile.profile_picture = profile_picture

            guest.user.save()
            guest.save()  # Save guest profile changes

    context = {
        'guest': guest,
        'user': user_profile.user,
        'email': user_profile.email,
        'can_edit': can_edit,
    }
    return render(request, 'foodFinder/settings.html', context)

def team(request):
    return render(request, 'foodFinder/team.html')

def team_members(request):
    return render(request, 'foodFinder/teamMembers.html')

def save_cropped_image(request):
    if request.method == 'POST':
        cropped_image = request.FILES.get('cropped_image')
        if cropped_image:
            guest = request.user.guest
            guest.profile_picture = cropped_image
            guest.save()
            return JsonResponse({'message': 'Image successfully uploaded'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            # Generate a unique token
            token = get_random_string(20)
            PasswordResetToken.objects.create(user=user, token=token)  # Save the token to the database

            reset_link = f'http://yourdomain.com/reset-password/{token}/'

            # Send email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset email has been sent.')
        except User.DoesNotExist:
            messages.error(request, 'Email not associated with any user.')

    return render(request, 'foodFinder/request_password_reset.html')

def reset_password(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token)

        if token_obj.is_expired():
            messages.error(request, 'This password reset link has expired.')
            return redirect('request_password_reset')  # Redirect to the request form

        if request.method == 'POST':
            password = request.POST.get('password')
            user = token_obj.user  # Get the associated user

            user.set_password(password)
            user.save()

            # Optionally, delete the token after successful use
            token_obj.delete()

            messages.success(request, 'Your password has been reset successfully!')
            return redirect('login')  # Redirect to login page after resetting

    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid token.')

    return render(request, 'foodFinder/reset_password.html', {'token': token})

def place_detail(request, place_id):
    place = get_object_or_404(Restaurant, id=place_id)
    reviews = place.reviews.all()  # Assuming there's a relationship to reviews
    return render(request, 'restaurant_detail.html', {
        'restaurant': place,
        'reviews': reviews,
    })