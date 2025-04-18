import random
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import TarotCard, Product
from .models import DailyCardDraw

@login_required
def profile_view(request):
    today = date.today()

    # Find tarot product in the database
    tarot_products = Product.objects.filter(
        category__name__iexact='tarotcards'
    )

    # Pick a random tarot product for the draw
    product_for_draw = None
    if tarot_products.exists():
        product_for_draw = random.choice(list(tarot_products))

    
    all_cards = list(TarotCard.objects.all())
    card_for_draw = random.choice(all_cards) if all_cards else None

    # Create or get the daily card draw for the user
    daily_draw, created = DailyCardDraw.objects.get_or_create(
        user=request.user,
        drawn_at=today,
        defaults={
            'product': product_for_draw,
            'card':    card_for_draw,
        }
    )

    # If the draw already exists, we don't want to create a new one
    prev_draws = (
        DailyCardDraw.objects
        .filter(user=request.user)
        .exclude(pk=daily_draw.pk)
        .order_by('-drawn_at')[:5]
    )

    context = {
        'latest_draw':  daily_draw,
        'recent_draws': prev_draws,
    }
    return render(request, 'accounts/profile.html', context)
