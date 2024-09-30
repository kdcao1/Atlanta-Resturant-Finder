from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, blank=True)
    zipcode = models.CharField(max_length=10, default="00000", blank=True)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=0.25)