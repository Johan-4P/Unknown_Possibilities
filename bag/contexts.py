from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for key, item in bag.items():

        if isinstance(item, int):
            product = get_object_or_404(Product, pk=key)
            quantity = item
            subtotal = quantity * product.price
            total += subtotal
            product_count += quantity
            bag_items.append({
                'key': key,
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
                'is_reading': False,
            })
        else:
            # Handle reading items with date and time
            product = get_object_or_404(Product, pk=item['item_id'])
            quantity = item['quantity']
            subtotal = quantity * product.price
            total += subtotal
            product_count += quantity
            bag_items.append({
                'key': key,
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
                'date': item.get('date'),
                'time': item.get('time'),
                'is_reading': item.get('is_reading', False),
            })
            
    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': total,
    }


