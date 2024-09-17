from django import forms
from .models import Guests

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Guests
        fields = ['profile_picture', 'zipcode', 'favorite_restaurants']