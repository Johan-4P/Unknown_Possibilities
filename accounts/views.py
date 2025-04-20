import random
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import TarotCard, Product
from .models import DailyCardDraw
from checkout.models import Order
from accounts.models import UserProfile

@login_required
def profile_view(request):
    today = date.today()

    # User profile
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Tarot-cards
    tarot_products = Product.objects.filter(category__name__iexact='tarotcards')
    product_for_draw = random.choice(list(tarot_products)) if tarot_products.exists() else None

    all_cards = list(TarotCard.objects.all())
    card_for_draw = random.choice(all_cards) if all_cards else None

    # DailyCardDraw
    daily_draw, _ = DailyCardDraw.objects.get_or_create(
        user=request.user,
        drawn_at=today,
        defaults={'product': product_for_draw, 'card': card_for_draw}
    )

    # If the daily draw already exists, we don't need to create a new one
    prev_draws = (
        DailyCardDraw.objects
        .filter(user=request.user)
        .exclude(pk=daily_draw.pk)
        .order_by('-drawn_at')[:5]
    )

    
    orders = Order.objects.filter(user_profile=user_profile).order_by('-date')

    context = {
        'latest_draw':  daily_draw,
        'recent_draws': prev_draws,
        'orders':       orders,
    }

    return render(request, 'accounts/profile.html', context)
