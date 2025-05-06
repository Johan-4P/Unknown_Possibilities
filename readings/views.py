from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking
from datetime import time, datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


@login_required
def book_reading(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        logger.warning("Form received: %s", request.POST)

        if form.is_valid():
            logger.warning("Form is valid")
            time_str = request.POST.get('time')
            try:
                booking_time = time.fromisoformat(time_str)
            except ValueError:
                logger.error("Invalid time format: %s", time_str)
                messages.error(request, "Invalid time format.")
                return redirect('book_reading')

            date = form.cleaned_data['date']
            reading_type = form.cleaned_data['reading_type']
            duration = int(form.cleaned_data['duration'])

            start_dt = datetime.combine(date, booking_time)
            end_dt = start_dt + timedelta(minutes=duration)

            bookings = Booking.objects.filter(
                date=date, reading_type=reading_type)
            for existing in bookings:
                existing_start = datetime.combine(existing.date, existing.time)
                existing_end = existing_start + timedelta(
                    minutes=existing.duration)

                if start_dt < existing_end and end_dt > existing_start:
                    logger.warning("Time %s", existing)
                    messages.error(
                        request, "This time slot overlaps,"
                        "with an existing booking.")
                    return redirect('book_reading')

            booking = form.save(commit=False)
            booking.time = booking_time
            booking.user = request.user

            # Set the price based on duration
            price_map = {15: 30.00, 30: 45.00, 60: 80.00}
            booking.price = price_map.get(duration, 0)

            booking.save()
            logger.warning("Booking saved: %s", booking)

            messages.success(request, "Your booking was successful!")
            return redirect('view_bag')
        else:
            logger.error("Form not valid: %s", form.errors)
            messages.error(request, "Something went wrong.")
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
