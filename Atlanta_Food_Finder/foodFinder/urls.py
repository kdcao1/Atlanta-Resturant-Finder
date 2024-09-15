import django.contrib.auth
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.logins, name="login"),
    path("settings/", views.settings, name="settings"),
    path("favorites/", views.favorites, name="favorites"),
]