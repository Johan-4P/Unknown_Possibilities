from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag_view, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<key>/', views.remove_from_bag, name='remove_from_bag'),
    path('bag/clear/', views.clear_bag, name='clear_bag'),

]
