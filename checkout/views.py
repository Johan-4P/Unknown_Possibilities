from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Order
from .forms import OrderForm
from bag.contexts import bag_contents
from products.models import Product
from checkout.models import OrderLineItem
from accounts.models import UserProfile

import json
import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key

    # Create PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # SetupIntent if logged in
    setup_intent = None
    if request.user.is_authenticated:
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if not user_profile.stripe_customer_id:
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.get_full_name(),
            )
            user_profile.stripe_customer_id = customer.id
            user_profile.save()
        else:
            customer = stripe.Customer.retrieve(user_profile.stripe_customer_id)

        setup_intent = stripe.SetupIntent.create(customer=customer.id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.stripe_pid = intent.id
            order.original_bag = json.dumps(bag)

            if request.user.is_authenticated:
                order.user_profile = user_profile

            order.save()

            # Save delivery info to profile if checkbox is selected
            if form.cleaned_data.get('save_info') and request.user.is_authenticated:
                user_profile.phone_number = form.cleaned_data['phone_number']
                user_profile.address = form.cleaned_data['street_address1']
                user_profile.street_address2 = form.cleaned_data['street_address2']
                user_profile.town_or_city = form.cleaned_data['town_or_city']
                user_profile.postcode = form.cleaned_data['postcode']
                user_profile.country = form.cleaned_data['country']
                user_profile.save()

            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    quantity = item_data['quantity'] if isinstance(item_data, dict) else item_data

                    if product.stock is not None:
                        product.stock = max(0, product.stock - quantity)
                        product.save()

                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                except Product.DoesNotExist:
                    messages.error(request, "One of the products wasn't found.")
                    order.delete()
                    return redirect(reverse('view_bag'))

            order.update_total()
            return redirect('checkout_success', order_number=order.order_number)
        else:
            messages.error(request, "There was an error with your form. Please double-check.")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            try:
                profile = request.user.userprofile
                initial_data = {
                    'full_name':        request.user.get_full_name(),
                    'email':            request.user.email,
                    'phone_number':     profile.phone_number,
                    'street_address1':  profile.street_address1,
                    'street_address2':  profile.street_address2,
                    'town_or_city':     profile.town_or_city,
                    'postcode':         profile.postcode,
                    'country':          profile.country,
                }

                if profile.phone_number or profile.street_address1:
                    initial_data['save_info'] = True

            except UserProfile.DoesNotExist:
                pass

        form = OrderForm(initial=initial_data)



    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'setup_client_secret': setup_intent.client_secret if setup_intent else None,
        **current_bag,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Send confirmation email
    subject = f"Order Confirmation - {order.order_number}"
    body = render_to_string('checkout/email/order_confirmation.txt', {'order': order})
    html_body = render_to_string('checkout/email/order_confirmation.html', {'order': order})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        html_message=html_body
    )

    request.session['bag'] = {}
    messages.success(request, f'Order {order_number} confirmed! A confirmation email was sent to {order.email}.')
    return render(request, 'checkout/checkout_success.html', {'order': order})
