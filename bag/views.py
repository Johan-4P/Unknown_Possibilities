from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def bag_view(request):
    """ A view that renders the shopping bag contents """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    print("POST data:", request.POST)

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    date = request.POST.get('date')
    time = request.POST.get('time')
    duration = request.POST.get('duration')

    bag = request.session.get('bag', {})

    # Price mapping for different durations
    DURATION_PRICES = {
        '20': 30,
        '30': 45,
        '60': 80,
    }

    if product.category.name.lower() == "readings" and date and time and duration:
        variant_key = f"{item_id}_{date}_{time}_{duration}"
        price = DURATION_PRICES.get(duration, product.price)  # fallback to product price if duration not found

        bag[variant_key] = {
            'item_id': item_id,
            'quantity': quantity,
            'date': date,
            'time': time,
            'duration': duration,
            'price': price,
            'is_reading': True,
        }

        messages.success(
            request, f"Added {product.name} ({duration} min) on {date} at {time} to your bag!"
        )
    else:
        if str(item_id) in bag:
            bag[str(item_id)]['quantity'] += quantity
            messages.success(request, f"Updated {product.name} quantity to {bag[str(item_id)]['quantity']}")
        else:
            bag[str(item_id)] = {'quantity': quantity, 'is_reading': False}
            messages.success(request, f"Added {product.name} to your bag")

    request.session['bag'] = bag
    return redirect(redirect_url)




def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.info(request, f'Updated {product.name} quantity to {quantity}')
    else:
        bag.pop(item_id)
        messages.warning(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect('view_bag')


def remove_from_bag(request, key):
    """Remove the item from the shopping bag"""
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
            if product:
                messages.success(request, f"Removed {product.name} from your bag.")
            else:
                messages.success(request, "Item removed from your bag.")
        else:
            messages.warning(request, "Item not found in your bag.")

        return redirect('view_bag')

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return redirect('view_bag')

