from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class Restaurant(models.Model):
    placeId = models.CharField(max_length=100)


class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)  # Optional
    last_name = models.CharField(max_length=100, blank=True)   # Optional
    location = models.CharField(max_length=100, blank=True)  # Optional
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, blank=True)


    def __str__(self):
        return self.user.username

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=0.25)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    favorite_restaurants = models.ManyToManyField('Restaurant', blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# Signal to create or update the UserProfile whenever the User is created or save
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
