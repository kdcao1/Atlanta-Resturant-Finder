import django.contrib.auth
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.logins, name="login"),
    path("settings/", views.settings, name="settings"),
    path("favorites/", views.favorites, name="favorites"),
    path("register/", views.register, name="register")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)