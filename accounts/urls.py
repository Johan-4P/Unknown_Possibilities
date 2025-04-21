from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('product-management/', views.product_management_view, name='product_management'),
]
