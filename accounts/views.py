import random
import stripe
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import TarotCard, Product
from .models import DailyCardDraw
from checkout.models import Order
from accounts.models import UserProfile
from products.forms import ProductForm
from .forms import UserProfileForm
from django.conf import settings

@login_required
def profile_view(request):
    today = date.today()
    stripe.api_key = settings.STRIPE_SECRET_KEY

    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your delivery information was updated!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    saved_card = None
    if user_profile.stripe_customer_id:
        payment_methods = stripe.PaymentMethod.list(
            customer=user_profile.stripe_customer_id,
            type="card",
        )
        if payment_methods.data:
            card_info = payment_methods.data[0].card
            saved_card = {
                'brand': card_info.brand,
                'last4': card_info.last4,
                'exp_month': card_info.exp_month,
                'exp_year': card_info.exp_year,
            }


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
        'user_profile': user_profile,
        'form': form,
        'orders': orders,
        'latest_draw': daily_draw,
        'recent_draws': prev_draws,
        'saved_card': saved_card,
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def edit_delivery_info(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your delivery info was updated!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/edit_delivery_info.html', {'form': form})


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def product_management(request):
    products = Product.objects.all()
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product added successfully!")
        return redirect('product_management')
    return render(request, 'accounts/product_management.html', {
        'products': products,
        'form': form
    })

@require_POST
@login_required
@user_passes_test(is_superuser)
def update_stock(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        new_stock = int(request.POST.get('stock'))
        product.stock = new_stock
        product.save()
        messages.success(request, f"Stock for {product.name} updated to {new_stock}.")
    except (ValueError, TypeError):
        messages.error(request, "Invalid stock value.")
    return redirect('product_management')

@login_required
@user_passes_test(is_superuser)
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect('product_management')
    return render(request, 'accounts/edit_product.html', {'form': form, 'product': product})

@require_POST
@login_required
@user_passes_test(is_superuser)
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect('product_management')

@login_required
@user_passes_test(is_superuser)
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "New product added!")
        return redirect('product_management')
    return render(request, 'accounts/add_product.html', {'form': form})

