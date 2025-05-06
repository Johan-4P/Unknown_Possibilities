from django.urls import path
from . import views

urlpatterns = [
    path('book-reading/',
         views.book_reading, name='book_reading'),
    path('get-booked-times/',
         views.get_booked_times, name='get_booked_times'),
    path('api/booked-times/',
         views.get_booked_times, name='get_booked_times'),
]
