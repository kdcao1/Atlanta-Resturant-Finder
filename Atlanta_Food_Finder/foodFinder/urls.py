from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.logins, name="login"),
    path("settings/", views.settings, name="settings"),
    path("favorites/", views.favorites, name="favorites"),
    path("register/", views.register, name="register"),
    path("save-cropped-image/", views.save_cropped_image, name="save_cropped_image"),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)