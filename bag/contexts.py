from .utils import bag_contents
from django.conf import settings


def toast_product_context(request):
    toast_product = request.session.get('toast_product')
    request.session.modified = True
    free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD

    # Get the bag data from the session
    bag_data = bag_contents(request)
    total = bag_data.get('grand_total', 0)
    delivery = bag_data.get('delivery', 0)

    # Calculate the total cost of the bag
    diff_to_free = None
    try:
        remaining = round(free_delivery_threshold - total, 2)
        if remaining > 0:
            diff_to_free = remaining
    except Exception:
        pass

    # Calculate the delivery cost
    delivery = calculate_shipping(total)

    # Send the data to the template context
    return {
        'toast_product': toast_product,
        'free_delivery_threshold': free_delivery_threshold,
        'diff_to_free': diff_to_free,
        'grand_total': total + delivery,
        'delivery': delivery,
    }


def calculate_shipping(total):
    if total == 0:
        return 0
    return round(total * settings.STANDARD_DELIVERY_PERCENTAGE / 100, 2)
