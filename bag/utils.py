from django.shortcuts import get_object_or_404
from products.models import Product



def bag_contents(request):
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    product_count = 0

    DURATION_PRICES = {
        '20': 30,
        '30': 45,
        '60': 80,
    }

    for key, item in bag.items():
       
        if isinstance(item, dict) and not item.get('is_reading', False):
            try:
                product = get_object_or_404(Product, pk=key)
            except:
                continue

            quantity = item.get('quantity', 1)
            subtotal = quantity * product.price
            total += subtotal
            product_count += quantity

            bag_items.append({
                'key': key,
                'product': product,
                'quantity': quantity,
                'unit_price': product.price,
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
            date = item.get('date')
            time = item.get('time')
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
                'date': date,
                'time': time,
                'duration': duration,
                'is_reading': True,
                'description': f"{product.name} ({duration} min) on {date} at {time}",
            })

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': total,
    }