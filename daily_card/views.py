from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyCardDraw
from products.models import TarotCard, Product
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

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


@csrf_exempt
@login_required
def save_daily_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        card_name = data.get('card_name')
        product_id = data.get('product_id')
        card = TarotCard.objects.filter(name=card_name, product__id=product_id).first()
        product = Product.objects.filter(id=product_id).first()

        if card and product:
            draw, created = DailyCardDraw.objects.update_or_create(
                user=request.user,
                drawn_at=date.today(),
                product=product,
                defaults={'card': card}
            )
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)