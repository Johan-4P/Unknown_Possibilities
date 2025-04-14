from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    product_count = 0

    DURATION_PRICES = {
        '20': 15,
        '30': 25,
        '60': 40,
    }

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

        elif isinstance(item, dict) and 'item_id' in item:
            try:
                product = get_object_or_404(Product, pk=item['item_id'])
            except:
                continue

            quantity = item.get('quantity', 1)
            duration = item.get('duration')
            price = DURATION_PRICES.get(duration, product.price)
            subtotal = quantity * price
            total += subtotal
            product_count += quantity

            bag_items.append({
                'key': key,
                'product': product,
                'quantity': quantity,
                'unit_price': price,
                'subtotal': subtotal,
                'date': item.get('date'),
                'time': item.get('time'),
                'duration': duration,
                'is_reading': item.get('is_reading', True),
            })

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': total,
    }
