from django.db import models
from django.contrib.auth.models import User
from products.models import TarotCard
from datetime import date


class DailyCardDraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    card = models.ForeignKey(
        'products.TarotCard', on_delete=models.SET_NULL, null=True)
    drawn_at = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.user.username} - {
            self.card.name} from {self.product.name} on {self.drawn_at}"
