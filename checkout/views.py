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
from django.contrib.auth.decorators import login_required



import json
import stripe
import datetime


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
            customer = stripe.Customer.retrieve(
                user_profile.stripe_customer_id)

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

            if form.cleaned_data.get(
                    'save_info') and request.user.is_authenticated:
                user_profile.phone_number = form.cleaned_data['phone_number']
                user_profile.address = form.cleaned_data['street_address1']
                user_profile.street_address2 = form.cleaned_data[
                    'street_address2']
                user_profile.town_or_city = form.cleaned_data['town_or_city']
                user_profile.postcode = form.cleaned_data['postcode']
                user_profile.country = form.cleaned_data['country']
                user_profile.save()

            for item_id, item_data in bag.items():
                try:
                    parts = item_id.split('_')
                    product_id = parts[0]
                    booking_date = parts[1] if len(parts) > 1 else None
                    booking_time = parts[2] if len(parts) > 2 else None
                    session_length = parts[3] if len(parts) > 3 else None

                    product = Product.objects.get(id=product_id)
                    quantity = item_data[
                        'quantity'] if isinstance(
                        item_data, dict) else item_data

                    if booking_date:
                        booking_date = datetime.datetime.strptime(
                            booking_date, "%Y-%m-%d").date()
                    if booking_time:
                        booking_time = datetime.datetime.strptime(
                            booking_time, "%H:%M").time()
                    if session_length:
                        session_length = int(session_length)

                    if product.category.name.lower(
                    ) == 'readings' and booking_date and booking_time:
                        conflict = OrderLineItem.objects.filter(
                            product=product,
                            booking_date=booking_date,
                            booking_time=booking_time
                        ).exists()

                        if conflict:
                            messages.error(
                                request,
                                f"{product.name} is already booked for {
                                    booking_date} at {booking_time}."
                            )
                            order.delete()
                            return redirect(reverse('view_bag'))

                    if product.stock is not None:
                        product.stock = max(0, product.stock - quantity)
                        product.save()

                    line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        booking_date=booking_date,
                        booking_time=booking_time,
                        session_length=session_length,
                    )
                    line_item.save()

                except Product.DoesNotExist:
                    messages.error(
                        request, "One of the products wasn't found.")
                    order.delete()
                    return redirect(reverse('view_bag'))

            order.update_total()
            request.session['order_number'] = order.order_number
            return redirect('checkout_success')

        else:
            messages.error(
                request, "There was an error with your form. "
                         "Please double-check.")

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
            'setup_client_secret':
                setup_intent.client_secret if setup_intent else None,
            **current_bag,
        }

    return render(request, 'checkout/checkout.html', context)

@login_required
def checkout_success(request):
    # Get order number from session
    order_number = request.session.get('order_number')

    if not order_number:
        messages.error(request, "There was an error with your order.")
        return redirect('home')

    order = get_object_or_404(Order, order_number=order_number)

    # Check if the order belongs to the logged-in user
    if order.user_profile and order.user_profile.user != request.user:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('home')

    # Send confirmation email
    subject = f"Order Confirmation - {order.order_number}"
    body = render_to_string(
        'checkout/email/order_confirmation.txt', {'order': order})
    html_body = render_to_string(
        'checkout/email/order_confirmation.html', {'order': order})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        html_message=html_body
    )

    # Clear the bag from the session
    request.session['bag'] = {}
    del request.session['order_number']

    messages.success(
        request,
        f'Order {order.order_number} confirmed! A confirmation email was sent to {order.email}.'
    )

    return render(request, 'checkout/checkout_success.html', {'order': order})
