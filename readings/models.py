from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):
    READING_CHOICES = [
        ('tarot', 'Tarot Reading'),
        ('rune', 'Rune Reading'),
        ('oracle', 'Oracle Reading'),
    ]

    DURATION_CHOICES = [
        (15, '15 min'),
        (30, '30 min'),
        (60, '60 min'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading_type = models.CharField(max_length=100, choices=READING_CHOICES)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        unique_together = ('date', 'time', 'reading_type')


def __str__(self):
    return (
        f"{self.user.username} - {self.reading_type} "
        f"({self.duration}min) @ {self.date} {self.time}"
    )
