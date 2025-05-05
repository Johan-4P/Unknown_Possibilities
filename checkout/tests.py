from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from products.models import Product, Category
from checkout.models import Order

class CheckoutViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='General')
        self.product = Product.objects.create(
            name='Test Product',
            price=100,
            description='Test product',
            category=self.category
        )
        self.bag_url = reverse('checkout')
        self.success_url_template = 'checkout/checkout_success.html'

    def test_checkout_view_empty_bag_redirects(self):
        response = self.client.get(self.bag_url)
        self.assertRedirects(response, reverse('products'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("nothing in your bag" in msg.message.lower() for msg in messages))

    def test_checkout_view_loads_with_items(self):
        
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {'quantity': 1, 'is_reading': False}
        }
        session.save()

        response = self.client.get(self.bag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_success_view(self):
        
        order = Order.objects.create(
            full_name='John Doe',
            email='john@example.com',
            phone_number='123456789',
            street_address1='Test Street',
            town_or_city='Test City',
            postcode='12345',
            country='SE',
            original_bag='{}',
            stripe_pid='test_pid'
        )
        url = reverse('checkout_success', args=[order.order_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.success_url_template)
