from django import forms
from .models import Guest

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['profile_picture']