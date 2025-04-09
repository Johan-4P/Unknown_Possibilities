from django.shortcuts import render, get_object_or_404
from .models import Product, TarotCard, Category
from django.db.models import Q
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
        'tarotcards': 'images/card-back-tarot.jpg',
        'wandering-moon': 'images/card-back-oracle.jpg',
    }

    category_texts = {
    'tarotcards': "Let the cards guide your day with ancient Tarot wisdom.",
}

    intro_text = category_texts.get(category.name.lower(), "Draw a card and see what the universe holds.")

    card_back = category_back_images.get(category.name.lower(), 'images/card-back-default.jpg')

    context = {
        'product': product,
        'tarot_cards': tarot_cards,
        'card_back': card_back,
        'intro_text': intro_text,
    }

    return render(request, 'products/products_detail.html', context)


def add_to_cart(request, product_id):
    """Add a product to the cart."""
    pass


def all_tarot_cards(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    cards = TarotCard.objects.all()

    if query:
        cards = cards.filter(Q(name__icontains=query) | Q(message__icontains=query))

    if category_id:
        cards = cards.filter(categories__id=category_id)

    categories = Category.objects.all()

    context = {
        'cards': cards,
        'categories': categories,
        'current_query': query,
        'current_category': category_id,
    }
    return render(request, 'products/tarot_cards.html', context)