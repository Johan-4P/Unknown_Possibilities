from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking
from datetime import time

def book_reading(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            time_str = request.POST.get('time') 
            booking_time = time.fromisoformat(time_str)  
            if booking_time < time(9, 0) or booking_time > time(17, 0):
                messages.error(request, "Bookings can only be made between 09:00 and 17:00.")
            else:
                date = form.cleaned_data['date']
                reading_type = form.cleaned_data['reading_type']

                if Booking.objects.filter(date=date, time=time_str, reading_type=reading_type).exists():
                    messages.error(request, "This time slot is already booked.")
                else:
                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.time = time_str
                    booking.save()
                    messages.success(request, "Your booking was successful!")
                    return redirect('view_bag')
    else:
        form = BookingForm()
    return render(request, 'readings/book_reading.html', {'form': form})
