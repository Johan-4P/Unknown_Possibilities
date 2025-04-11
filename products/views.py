from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, TarotCard, Category
from django.contrib import messages
from django.db.models import Q
import random
from django.db.models.functions import Lower

def all_product(request):
    """ A view to return all products """
    products = Product.objects.all()
    query = None
    categories = None
    direction = None
    sort = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
                    products = products.order_by(sortkey)
                else:
                    products = products.order_by(sortkey)

        if 'q' in request.GET:
            if 'category' in request.GET:
                categories = request.GET['category'].split(',')
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories)
                

            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries).distinct()
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_category': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def category_products(request, category_name):
    """ View to show products in a specific category """
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)

    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'products/products.html', context)



def products_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    category = product.category
    tarot_cards = TarotCard.objects.filter(categories=category) if request.user.is_authenticated else []


    


    category_texts = {
    'tarotcards': "Let the cards guide your day with ancient Tarot wisdom.",
}

    intro_text = category_texts.get(category.name.lower(), "Draw a card and see what the universe holds.")

    card_back = f'images/card-backs/card-back-{product.sku.lower()}.png'

    context = {
        'product': product,
        'tarot_cards': tarot_cards,
        'card_back': card_back,
        'intro_text': intro_text,
    }

    return render(request, 'products/products_detail.html', context)


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