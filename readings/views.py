from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm

def book_reading(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Your reading has been booked!")
            return redirect('view_bag')
    else:
        form = BookingForm()
    return render(request, 'readings/book_reading.html', {'form': form})
