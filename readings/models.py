from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    READING_CHOICES = [
        ('tarot', 'Tarot Reading'),
        ('rune', 'Rune Reading'),
        ('oracle', 'Oracle Reading'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading_type = models.CharField(max_length=20, choices=READING_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reading_type} @ {self.date} {self.time}"
