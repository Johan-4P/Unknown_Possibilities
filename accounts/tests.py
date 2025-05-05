from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))  
        self.assertRedirects(response, '/accounts/login/?next=/accounts/')

    def test_logged_in_user_can_access_profile(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

class ProductManagementViewTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')
        self.user = User.objects.create_user(username='normaluser', password='testpass')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('product_management'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/product-management/')

def test_forbidden_for_non_superuser(self):
    self.client.login(username='normaluser', password='testpass')
    response = self.client.get(reverse('product_management'))
    self.assertEqual(response.status_code, 403)

    def test_superuser_can_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('product_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/product_management.html')
