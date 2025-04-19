from django import forms
from .models import Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class OrderForm(forms.ModelForm):
    save_info = forms.BooleanField(
        required=False,
        label="Save this information for next time",
    )

    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'address',
            'country',
            'postcode',
            'town_or_city',
        )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'full_name',
            'email',
            'phone_number',
            'address',
            'country',
            'postcode',
            'town_or_city',
            
        )

        
        self.fields['save_info'].widget.attrs.update({
            'class': 'form-check-input me-2',
        })
