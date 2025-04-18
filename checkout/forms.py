from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 'address', 'country', 'postcode', 'town_or_city')

    def _init__(self, *args, **kwargs):
        """"Add placeholders and classes, remove auto-generated labels and set autofocus on first field."""

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'country': 'Country',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholders = f'{placeholders} *'
            else:
                placeholders = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


# checkout/forms.py
from django import forms

class CheckoutForm(forms.Form):
    full_name    = forms.CharField(max_length=100)
    email        = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    address      = forms.CharField(widget=forms.Textarea)
    

    save_info = forms.BooleanField(
        required=False,
        label="Save this information for next time",
    )
