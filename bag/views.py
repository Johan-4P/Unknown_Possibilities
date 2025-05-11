from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from products.models import Product
from readings.models import Booking
import pprint


def bag_view(request):
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0

    for key, item_data in bag.items():
        try:
            # Check if item_data is a dictionary or a simple quantity
            product_id = item_data.get(
                'item_id') if isinstance(item_data, dict) else int(key)
            if not product_id:
                product_id = int(key)

            product = get_object_or_404(Product, pk=int(product_id))

            if isinstance(item_data, dict):
                quantity = item_data.get('quantity', 1)
                price = item_data.get('price', product.price)
                is_reading = item_data.get('is_reading', False)
                date = item_data.get('date')
                time = item_data.get('time')
                duration = item_data.get('duration')
            else:
                quantity = item_data
                price = product.price
                is_reading = False
                date = time = duration = None

            subtotal = price * quantity
            total += subtotal

            bag_items.append({
                'key': key,  # This is the key used in the session
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal,
                'is_reading': is_reading,
                'date': date,
                'time': time,
                'duration': duration,
            })

        except Exception as e:
            print(f"[bag_view] Skipping item {key}: {e}")
            continue

    context = {
        'bag_items': bag_items,
        'total': total,
    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', reverse('products'))
    date = request.POST.get('date')
    time = request.POST.get('time')
    duration = request.POST.get('duration')

    bag = request.session.get('bag', {})

    DURATION_PRICES = {
        '15': 30,
        '30': 45,
        '60': 80,
    }

    # === READINGS ===
    if product.category.name.lower() == "readings":
        
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to book a reading.")
            return redirect('account_login')

        
        if not (date and time and duration):
            messages.error(request, "Missing booking information.")
            return redirect(redirect_url)

        variant_key = f"{item_id}_{date}_{time}_{duration}"
        price = DURATION_PRICES.get(duration, product.price)

        
        bag[variant_key] = {
            'item_id': item_id,
            'quantity': quantity,
            'date': date,
            'time': time,
            'duration': duration,
            'price': price,
            'is_reading': True,
        }

        from datetime import datetime, time as time_module

        try:
            booking_time_obj = time_module.fromisoformat(time)
            booking_date_obj = datetime.strptime(date, "%Y-%m-%d").date()

            if not Booking.objects.filter(
                date=booking_date_obj,
                time=booking_time_obj,
                reading_type=product.name,
                user=request.user
            ).exists():
                Booking.objects.create(
                    user=request.user,
                    reading_type=product.name,
                    duration=int(duration),
                    date=booking_date_obj,
                    time=booking_time_obj,
                    price=price,
                    message=f"Auto-booked from product '{product.name}'",
                )
                messages.success(
                    request,
                    f"Booking for {product.name} at {time} on {date} created!"
                )
            else:
                messages.info(
                    request, f"You already have a booking for {product.name} at {time} on {date}."
                )

        except Exception as e:
            messages.error(request, f"Error creating booking: {e}")

        request.session['toast_product'] = {
            'name': product.name,
            'image_url': product.image.url if product.image else '',
            'qty': 1,
            'total': str(price),
            'duration': duration,
            'date': date,
            'time': time,
            'is_reading': True,
        }

    # === PRODUCTS ===
    else:
        item_id_str = str(item_id)
        if item_id_str in bag:
            if isinstance(bag[item_id_str], dict):
                bag[item_id_str]['quantity'] += quantity
            else:
                bag[item_id_str] = {
                    'quantity': bag[item_id_str] + quantity,
                    'is_reading': False
                }
        else:
            bag[item_id_str] = {
                'quantity': quantity,
                'is_reading': False
            }

        messages.success(request, f"Added {product.name} to your bag!")

        request.session['toast_product'] = {
            'name': product.name,
            'image_url': product.image.url if product.image else '',
            'qty': quantity,
            'total': str(product.price * quantity),
            'is_reading': False,
        }

    request.session['bag'] = bag
    return redirect(redirect_url)



def adjust_bag(request, item_id):
    bag = request.session.get('bag', {})
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    item_id_str = str(item_id)

    if quantity > 0:
        if isinstance(bag.get(item_id_str), dict):
            bag[item_id_str]['quantity'] = quantity
        else:
            bag[item_id_str] = {'quantity': quantity, 'is_reading': False}
        messages.info(
            request, f'Updated {product.name} quantity to {quantity}')
    else:
        bag.pop(item_id_str, None)
        messages.warning(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect('view_bag')


def remove_from_bag(request, key):
    try:
        bag = request.session.get('bag', {})
        product = None

        item = bag.get(key)
        if isinstance(item, dict):
            product_id = item.get('item_id')
        else:
            product_id = key

        if product_id:
            product = get_object_or_404(Product, pk=product_id)

        if key in bag:
            del bag[key]
            request.session['bag'] = bag
            request.session.pop('toast_product', None)

            if product:
                messages.success(
                    request, f"Removed {product.name} from your bag.")
            else:
                messages.success(request, "Item removed from your bag.")
        else:
            messages.warning(request, "Item not found in your bag.")

        return redirect('view_bag')

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return redirect('view_bag')


def clear_bag(request):
    request.session['bag'] = {}
    messages.success(request, "Bag has been cleared.")
    return redirect('view_bag')
