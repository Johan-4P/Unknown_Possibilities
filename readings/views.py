from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking
from datetime import time, datetime, timedelta
from django.http import JsonResponse

def book_reading(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            time_str = request.POST.get('time')
            try:
                booking_time = time.fromisoformat(time_str)
            except ValueError:
                messages.error(request, "Invalid time format.")
                return redirect('book_reading')

            if booking_time < time(9, 0) or booking_time > time(17, 0):
                messages.error(request, "Bookings must be between 09:00 and 17:00.")
                return redirect('book_reading')

            date = form.cleaned_data['date']
            reading_type = form.cleaned_data['reading_type']
            duration = form.cleaned_data['duration']

            # Check if the booking already exists
            start_dt = datetime.combine(date, booking_time)
            end_dt = start_dt + timedelta(minutes=duration)

            # Check if the booking overlaps with existing bookings
            overlap = False
            bookings = Booking.objects.filter(date=date, reading_type=reading_type)
            for existing_booking in bookings:
                existing_start = datetime.combine(existing_booking.date, existing_booking.time)
                existing_end = existing_start + timedelta(minutes=existing_booking.duration)

                if (start_dt < existing_end and end_dt > existing_start):
                    overlap = True
                    break

            if overlap:
                messages.error(request, "This time slot overlaps with an existing booking.")
                return redirect('book_reading')

            booking = form.save(commit=False)
            booking.time = booking_time
            booking.user = request.user
            booking.save()
            messages.success(request, "Your booking was successful!")
            return redirect('view_bag')
    else:
        form = BookingForm()

    return render(request, 'readings/book_reading.html', {'form': form})

def get_booked_times(request):
    date = request.GET.get('date')
    reading_type = request.GET.get('reading_type')

    if not date or not reading_type:
        return JsonResponse({'booked_times': []})

    bookings = Booking.objects.filter(date=date, reading_type=reading_type)
    booked_slots = set()

    for booking in bookings:
        start_time = datetime.strptime(booking.time.strftime('%H:%M'), '%H:%M')
        duration = booking.duration  # assumed in minutes
        blocks = duration // 30

        for i in range(blocks):
            slot_time = start_time + timedelta(minutes=30 * i)
            time_str = slot_time.strftime('%H:%M')
            booked_slots.add(time_str)

    return JsonResponse({'booked_times': list(booked_slots)})
