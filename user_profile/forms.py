from django import forms
from .models import UserProfile, SavedAddress

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'city', 'state', 'postal_code', 'profile_picture']

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = SavedAddress
        fields = ['address']