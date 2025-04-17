from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyCardDraw
from products.models import TarotCard, Product
from datetime import date

def draw_card_of_the_day(request, product_id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    product = get_object_or_404(Product, pk=product_id)

    already_drawn = False
    if not request.user.is_superuser:
        already_drawn = DailyCardDraw.objects.filter(
            user=request.user,
            product=product,
            drawn_at=date.today()
        ).exists()

    cards = list(TarotCard.objects.filter(product=product).order_by('?')[:5])

    context = {
        'cards': cards,
        'product': product,
        'card_back': f'images/card-backs/card-back-{product.sku.lower()}.png',
        'already_drawn': already_drawn,
    }

    return render(request, 'daily_card/card_of_the_day.html', context)




def choose_deck(request):
    decks = Product.objects.filter(category__name__iexact='tarotcards')
    return render(request, 'daily_card/choose_deck.html', {'decks': decks})
