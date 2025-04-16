from django.shortcuts import render, redirect
from .models import DailyCardDraw
from products.models import TarotCard, Product, Category
from datetime import date
import random

def draw_card_of_the_day(request, product_id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    existing = DailyCardDraw.objects.filter(
    user=request.user,
    product_id=product_id,
    drawn_at=date.today()
).first()

    if existing:
        card = existing.card
    else:
        cards = TarotCard.objects.filter(product_id=product_id)
        card = random.choice(cards)
        DailyCardDraw.objects.create(user=request.user, card=card)
    already_drawn = existing is not None
    return render(request, 'daily_card/card_of_the_day.html', {'card': card, 'already_drawn': already_drawn})


def choose_deck(request):
    decks = Product.objects.filter(category__name__iexact='tarotcards')
    return render(request, 'daily_card/choose_deck.html', {'decks': decks})