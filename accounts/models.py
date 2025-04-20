# accounts/models.py
from django.contrib.auth.models import User
from django.db import models
from daily_card.models import DailyCardDraw


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address     = models.CharField(max_length=255, blank=True)
   

    def __str__(self):
        return f"{self.user.username}’s profile"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional fields can be added here
    def __str__(self):
        return self.user.username