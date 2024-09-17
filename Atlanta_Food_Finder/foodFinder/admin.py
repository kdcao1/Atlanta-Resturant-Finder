from django.contrib import admin

# Register your models here.

from .models import Guests, Restaurant
admin.site.register(Guests)
admin.site.register(Restaurant)