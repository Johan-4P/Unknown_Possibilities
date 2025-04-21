# accounts/models.py
from django.contrib.auth.models import User
from django.db import models
from daily_card.models import DailyCardDraw
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
   

    def __str__(self):
        return f"{self.user.username}’s profile"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.user.username
