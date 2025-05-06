from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product, Category, TarotCard
from daily_card.models import DailyCardDraw
import json

User = get_user_model()


class DailyCardTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Tarotcards')
        self.product = Product.objects.create(
            name='Mystic Tarot Deck',
            price=100,
            description='A mystical tarot deck',
            category=self.category,
            sku='MTD001'
        )
        self.card = TarotCard.objects.create(
            name='The Fool',
            product=self.product,
            message='A new beginning'
        )
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_choose_deck_view(self):
        response = self.client.get(reverse('choose_deck'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daily_card/choose_deck.html')

    def test_draw_card_redirects_if_not_logged_in(self):
        url = reverse('card_of_the_day', args=[self.product.id])
        response = self.client.get(url)
        self.assertRedirects(response, '/accounts/login/?next=' + url)

    def test_draw_card_view_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('card_of_the_day', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daily_card/card_of_the_day.html')

    def test_save_daily_card(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('save_daily_card')
        data = {
            'card_name': self.card.name,
            'product_id': self.product.id
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})
        self.assertTrue(DailyCardDraw.objects.filter(
            user=self.user, product=self.product).exists())
