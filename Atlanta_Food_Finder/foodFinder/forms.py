from django import forms
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['profile_picture', 'location', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Set the initial value of the email field if the user instance is available
        if kwargs.get('instance') and kwargs['instance'].user:
            self.initial['email'] = kwargs['instance'].user.email

class Favorite(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['favorite_restaurants']