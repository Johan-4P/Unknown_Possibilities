from django.shortcuts import render, get_object_or_404
from .models import Product, TarotCard
import random

def all_product(request):
    """ A view to return all products """
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)


def products_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    category = product.category
    tarot_cards = TarotCard.objects.filter(categories=category) if request.user.is_authenticated else []


    
    category_back_images = {
        'light-seers': 'images/card-back-tarot.jpg',
        'wandering-moon': 'images/card-back-oracle.jpg',
    }

    category_texts = {
    'tarot': "Let the cards guide your day with ancient Tarot wisdom.",
}

    intro_text = category_texts.get(category.name.lower(), "Draw a card and see what the universe holds.")

    card_back = category_back_images.get(category.name.lower(), 'images/card-back-default.jpg')

    context = {
        'product': product,
        'tarot_cards': tarot_cards,
        'card_back': card_back,
        'intro_text': intro_text,
    }

    return render(request, 'products/product_detail.html', context)

