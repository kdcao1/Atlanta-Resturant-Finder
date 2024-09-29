from django.shortcuts import render, redirect
from .models import Guest
from .forms import ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from .models import PasswordResetToken  # Import the new model



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


@login_required
def settings(request):
    guest = Guest.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=guest)

        cropped_image_data = request.POST.get('cropped_image_data', None)

        if form.is_valid():
            if cropped_image_data:
                from django.core.files.base import ContentFile
                import base64

                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{guest.user.username}_profile.{ext}')

                guest.profile_picture = data
                guest.save()

            form.save()
            return redirect('settings')
    else:
        form = ProfileForm(instance=guest)

    context = {
        'form': form,
        'guest': guest,
    }
    return render(request, 'foodFinder/settings.html', context)

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
