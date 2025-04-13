from django.urls import path
from . import views

urlpatterns = [
    path('book-reading/', views.book_reading, name='book_reading'),
]
