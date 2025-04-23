from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_deck, name='choose_deck'),
    path('<int:product_id>/', views.draw_card_of_the_day, name='card_of_the_day'),
    path('save_daily_card/', views.save_daily_card, name='save_daily_card'),
]
