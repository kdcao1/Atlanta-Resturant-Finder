from django.contrib import admin

# Register your models here.

from .models import Guest, Restaurant
admin.site.register(Guest)
admin.site.register(Restaurant)
