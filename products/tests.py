from django.test import TestCase
from .models import Product
from django.urls import reverse


class ProductModelTest(TestCase):

    def test_product_str_returns_name(self):
        product = Product.objects.create(name='Test Crystal', price=100)
        self.assertEqual(str(product), 'Test Crystal')


class ProductListViewTest(TestCase):

    def setUp(self):
        Product.objects.create(name='Test Crystal', price=100)
        Product.objects.create(name='Test Tarot Deck', price=200)

    def test_products_page_status_code(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def test_products_page_template(self):
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, 'products/products.html')

    def test_search_functionality(self):
        response = self.client.get(reverse('products') + '?q=Tarot')
        self.assertContains(response, 'Test Tarot Deck')
        self.assertNotContains(response, 'Test Crystal')
