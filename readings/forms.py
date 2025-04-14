from django import forms
from .models import Booking
from datetime import time

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['reading_type', 'duration', 'date', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'reading_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        time_str = self.data.get('time')  
        if time_str:
            booking_time = time.fromisoformat(time_str)  
            if booking_time < time(9, 0) or booking_time > time(17, 0):
                raise forms.ValidationError("Bookings can only be made between 09:00 and 17:00.")
        return cleaned_data
