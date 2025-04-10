from django.urls import path
from . import views

urlpatterns = [
    path('tarotcards/', views.all_tarot_cards, name='tarotcards'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/', views.products_detail, name='product_detail'),
    path('', views.all_product, name='products'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),

]
