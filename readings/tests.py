from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from readings.models import Booking
from datetime import date, time
import json

User = get_user_model()

class ReadingsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book_url = reverse('book_reading')
        self.get_times_url = reverse('get_booked_times')

    def test_book_reading_redirect_if_not_logged_in(self):
        response = self.client.get(self.book_url)
        self.assertRedirects(response, '/accounts/login/?next=' + self.book_url)

    def test_book_reading_page_loads_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'readings/book_reading.html')

    def test_successful_booking(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'reading_type': 'tarot',
            'date': date.today().strftime('%Y-%m-%d'),
            'time': '10:00',
            'duration': 30
        }
        response = self.client.post(self.book_url, data, follow=True)
        self.assertRedirects(response, reverse('view_bag')) 
        self.assertTrue(Booking.objects.filter(user=self.user, reading_type='tarot').exists())

    def test_booking_conflict(self):

        existing_booking = Booking.objects.create(
            user=self.user,
            reading_type='tarot',
            date=date.today(),
            time=time(10, 0),
            duration=30,
            price=45
        )
        self.client.login(username='testuser', password='testpass')
        data = {
            'reading_type': 'tarot',
            'date': date.today().strftime('%Y-%m-%d'),
            'time': '10:00',
            'duration': 30
        }
        response = self.client.post(self.book_url, data, follow=True)
        messages = list(response.context['messages'])
        self.assertTrue(any("overlaps" in msg.message.lower() for msg in messages))

    def test_get_booked_times_api(self):
        Booking.objects.create(
            user=self.user,
            reading_type='tarot',
            date=date.today(),
            time=time(10, 0),
            duration=30,
            price=45
        )
        response = self.client.get(self.get_times_url, {'date': date.today().strftime('%Y-%m-%d'), 'reading_type': 'tarot'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('10:00', data['booked_times'])
