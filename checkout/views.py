# checkout/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import stripe

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents
from accounts.models import Profile

# Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """Handle the checkout process"""
    # 1) Get the bag from session
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect('products')

    # 2) Count the items in the bag and calculate total
    current_bag = bag_contents(request)
    stripe_total = round(current_bag['grand_total'] * 100)
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # 3) Handle the form submission
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # 3a) Create a new order instance but don't save it yet
            order = form.save(commit=False)

            # 3b) Attach the Stripe payment intent to the order
            if request.user.is_authenticated:
                profile, _ = Profile.objects.get_or_create(user=request.user)
                order.user_profile = profile

            order.original_bag = str(bag)
            order.stripe_pid = intent.id
            order.save()

            # Save the user's information if they are logged in and have opted to save it
            if form.cleaned_data.get('save_info') and request.user.is_authenticated:
                profile.phone_number = form.cleaned_data['phone_number']
                profile.address = form.cleaned_data['address']
                profile.save()

            # 4) Create order line items for each item in the bag
            for item_key, item_data in bag.items():
                try:
                    product_id = (
                        item_data.get('item_id') if isinstance(item_data, dict)
                        else int(item_key)
                    )
                    product = get_object_or_404(Product, pk=product_id)
                    quantity = (
                        item_data.get('quantity', 1) if isinstance(item_data, dict)
                        else item_data
                    )
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
                except Exception as e:
                    messages.error(request, f"One Error accrued: {e}")
                    order.delete()
                    return redirect('view_bag')

            # 5) Send confirmation email to the user
            subject = f"Orderbekräftelse #{order.order_number}"
            message_txt = render_to_string(
                'checkout/email/order_confirmation.txt',
                {'order': order}
            )
            message_html = render_to_string(
                'checkout/email/order_confirmation.html',
                {'order': order}
            )
            send_mail(
                subject,
                message_txt,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                html_message=message_html,
            )

            # 6) Empty the bag and redirect to success page
            request.session['bag'] = {}
            return redirect('checkout_success', order_number=order.order_number)

        else:
            messages.error(
                request,
                "There was an error with your form. Please check your information and try again."
            )

    # 7) GET: show checkout-form
    else:
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                initial = {
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'address': profile.address,
                }
            except Profile.DoesNotExist:
                initial = {}
        else:
            initial = {}

        form = OrderForm(initial=initial)

    # 8) Render checkout-page with form and Stripe data
    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
        **current_bag,  # bag_items, total, grand_total
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, order_number):
    """Show the checkout success page"""
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(
        request,
        f'Order is received {order_number}.'
    )
    return render(
        request,
        'checkout/checkout_success.html',
        {'order': order}
    )
