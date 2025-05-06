from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):

    def test_home_page_loads_correctly(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
