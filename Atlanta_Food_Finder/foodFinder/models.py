from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

class Guests(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, blank=True)
    zipcode = models.CharField(max_length=10, default="00000", blank=True)
