# checkout/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import stripe

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents
from accounts.models import Profile 

# Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """Show checkout page."""
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Din varukorg är tom.")
        return redirect('products')

    # calculate total and create PaymentIntent
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)  # i öre
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save order info to the database
            order = form.save(commit=False)
            order.original_bag = str(bag)
            order.stripe_pid = intent.id
            order.save()

            # Save profile info if user is authenticated and save_info is checked
            if form.cleaned_data.get('save_info') and request.user.is_authenticated:
                profile, _ = Profile.objects.get_or_create(user=request.user)
                profile.phone_number = form.cleaned_data['phone_number']
                profile.address      = form.cleaned_data['address']
                profile.save()

            # Create order line items
            for item_key, item_data in bag.items():
                try:
                    product_id = item_data.get('item_id') if isinstance(item_data, dict) else int(item_key)
                    product = get_object_or_404(Product, pk=product_id)
                    quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                    line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    line_item.save()
                except Exception as e:
                    messages.error(request, f"Error processing item: {e}")
                    order.delete()
                    return redirect('view_bag')

            # Empty the bag
            request.session['bag'] = {}
            return redirect('checkout_success', order_number=order.order_number)
        else:
            messages.error(request, "The form could not be validated. Please check your details.")
    else:
        # GET: initialize the form with user data if authenticated
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                initial = {
                    'full_name':    request.user.get_full_name(),
                    'email':        request.user.email,
                    'phone_number': profile.phone_number,
                    'address':      profile.address,
                }
            except Profile.DoesNotExist:
                initial = {}
        else:
            initial = {}
        form = OrderForm(initial=initial)

    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
        **current_bag
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """Confirmation view after successful order."""
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order received! Your order number is {order_number}.')
    return render(request, 'checkout/checkout_success.html', {'order': order})
