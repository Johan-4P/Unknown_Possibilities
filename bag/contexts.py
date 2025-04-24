from .utils import bag_contents
from django.conf import settings



def toast_product_context(request):
    toast_product = request.session.get('toast_product')
    request.session.modified = True
    free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD

    
    bag_data = bag_contents(request)
    total = bag_data.get('grand_total', 0)

    diff_to_free = None
    try:
        remaining = round(free_delivery_threshold - total, 2)
        if remaining > 0:
            diff_to_free = remaining
    except Exception:
        pass

    return {
        'toast_product': toast_product,
        'free_delivery_threshold': free_delivery_threshold,
        'diff_to_free': diff_to_free,
        'grand_total': total,
    }

