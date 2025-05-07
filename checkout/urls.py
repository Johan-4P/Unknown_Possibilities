from django.urls import path
from . import views
from .webhook_handler import stripe_webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout/success/',
        views.checkout_success,
        name='checkout_success'),

    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
]
