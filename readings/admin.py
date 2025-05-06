from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'reading_type', 'duration', 'date',
                    'time', 'price', 'created_at')
    list_filter = ('reading_type', 'date')
