from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Guests(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)