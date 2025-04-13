from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm

def book_reading(request):
    initial_data = {}
    reading_type = request.GET.get('type', '').lower()
    if reading_type in ['tarot', 'rune', 'oracle']:
        initial_data['reading_type'] = reading_type

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Your reading has been booked!")
            return redirect('view_bag')
    else:
        form = BookingForm(initial=initial_data)
    
    return render(request, 'readings/book_reading.html', {'form': form})

