from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def bag_view(request):
    """ A view that renders the shopping bag contents """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a product or reading with optional date/time to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    date = request.POST.get('date')
    time = request.POST.get('time')

    bag = request.session.get('bag', {})

    # Check if the product is a reading and has a date and time
    if product.category.name.lower() == "readings" and date and time:
        variant_key = f"{item_id}_{date}_{time}"
        bag[variant_key] = {
            'item_id': item_id,
            'quantity': quantity,
            'date': date,
            'time': time,
            'is_reading': True,
        }
        messages.success(request, f"Added {product.name} for {date} at {time} to your bag!")
    else:
        
        if item_id in bag:
            bag[item_id]['quantity'] += quantity
            messages.success(request, f"Updated {product.name} quantity to {bag[item_id]['quantity']}")
        else:
            bag[item_id] = {'quantity': quantity, 'is_reading': False}
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


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})

        bag.pop(item_id)
        request.session['bag'] = bag
        messages.warning(request, f'Removed {product.name} from your bag')

        return redirect('view_bag')

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect('view_bag')
