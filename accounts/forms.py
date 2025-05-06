from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
        )
        widgets = {
            'street_address1': forms.TextInput(
                attrs={'placeholder': 'Street Address 1'}),
            'street_address2': forms.TextInput(
                attrs={'placeholder': 'Street Address 2'}),
            'town_or_city': forms.TextInput(
                attrs={'placeholder': 'Town or City'}),
            'county': forms.TextInput(attrs={'placeholder': 'County'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }
