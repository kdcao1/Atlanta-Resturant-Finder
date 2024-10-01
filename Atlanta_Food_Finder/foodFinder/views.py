from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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



def home(request):
    if not request.user.is_authenticated:
        return redirect('/foodFinder/login/')
    else:
        favorite_restaurant_ids = request.user.guest.favorite_restaurants.values_list('id', flat=True)
        context = {
            'apiKey': os.getenv('GMAPS_API_KEY'),
            'favorite_restaurant_ids': favorite_restaurant_ids,
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



@login_required
def favorites(request):
    favorite_restaurants = request.user.guest.favorite_restaurants.all() if request.user.is_authenticated else []
    context = {
        'favorite_restaurants': favorite_restaurants,
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


@login_required
def settings(request):
    guest = Guest.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=guest)

        cropped_image_data = request.POST.get('cropped_image_data', None)

        if form.is_valid():
            # Handle profile picture cropping
            if cropped_image_data:
                from django.core.files.base import ContentFile
                import base64

                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{guest.user.username}_profile.{ext}')

                guest.profile_picture = data

            # Save guest profile and user details
            guest = form.save()
            user_profile.username = request.POST.get('username', user_profile.username)
            user_profile.email = request.POST.get('email', user_profile.email)
            user_profile.location = request.POST.get('location', user_profile.location)
            user_profile.bio = request.POST.get('bio', user_profile.bio)
            user_profile.first_name = request.POST.get('first_name', user_profile.first_name)
            user_profile.last_name = request.POST.get('last_name', user_profile.last_name)

            # Handle profile picture upload if provided
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                user_profile.profile_picture = profile_picture

            user_profile.save()  # Save user profile changes
            guest.save()  # Save guest profile changes
            return redirect('settings')  # Redirect to the settings page or another page after saving
    else:
        form = ProfileForm(instance=guest)

    context = {
        'form': form,
        'guest': guest,
        'user': user_profile.user,
        'email': user_profile.email,
        'location': user_profile.location,
        'bio': user_profile.bio,
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