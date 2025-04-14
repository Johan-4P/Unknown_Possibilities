from django import forms
from .models import Booking


def generate_time_choices():
    times = []
    for hour in range(9, 17):
        times.append((f"{hour:02d}:00", f"{hour:02d}:00"))
        times.append((f"{hour:02d}:30", f"{hour:02d}:30"))
    return times

class BookingForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=generate_time_choices(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['reading_type', 'duration', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'reading_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
        }
