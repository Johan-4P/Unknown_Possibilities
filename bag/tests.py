from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category


class BagViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Tarot Cards')

        self.product = Product.objects.create(
            name='Test Product',
            price=100,
            description='A test product',
            category=self.category
        )

    def test_bag_view_status_code(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 2, 'redirect_url': reverse('view_bag')}
        )
        session = self.client.session
        bag = session.get('bag')
        self.assertIn(str(self.product.id), bag)
        self.assertEqual(bag[str(self.product.id)]['quantity'], 2)
        self.assertRedirects(response, reverse('view_bag'))

    def test_adjust_bag(self):

        session = self.client.session
        session['bag'] = {str(
            self.product.id): {'quantity': 2, 'is_reading': False}}
        session.save()

        response = self.client.post(
            reverse('adjust_bag', args=[self.product.id]),
            {'quantity': 5}
        )
        session = self.client.session
        bag = session.get('bag')
        self.assertEqual(bag[str(self.product.id)]['quantity'], 5)
        self.assertRedirects(response, reverse('view_bag'))

    def test_remove_from_bag(self):

        session = self.client.session
        session['bag'] = {str(
            self.product.id): {'quantity': 2, 'is_reading': False}}
        session.save()

        response = self.client.get(
            reverse('remove_from_bag', args=[self.product.id]))
        session = self.client.session
        bag = session.get('bag')
        self.assertNotIn(str(self.product.id), bag)
        self.assertRedirects(response, reverse('view_bag'))

    def test_clear_bag(self):

        session = self.client.session
        session['bag'] = {str(
            self.product.id): {'quantity': 1, 'is_reading': False}}
        session.save()

        response = self.client.get(reverse('clear_bag'))
        session = self.client.session
        bag = session.get('bag')
        self.assertEqual(bag, {})
        self.assertRedirects(response, reverse('view_bag'))
