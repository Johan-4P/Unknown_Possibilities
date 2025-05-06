from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path(
        'product-management/',
        views.product_management,
        name='product_management'
    ),
    path(
        'product/<int:product_id>/update-stock/',
        views.update_stock,
        name='update_stock'
    ),
    path(
        'product/<int:product_id>/edit/',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'product/<int:product_id>/delete/',
        views.delete_product,
        name='delete_product'
    ),
    path('product/add/', views.add_product, name='add_product'),
    path(
        'edit-delivery-info/',
        views.edit_delivery_info,
        name='edit_delivery_info'
    ),
]
