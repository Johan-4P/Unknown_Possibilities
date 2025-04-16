from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect('products')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.original_bag = str(bag)
            order.stripe_pid = 'fake_pid' # Replace with actual Stripe PID
            order.save()

            for item_key, item_data in bag.items():
                try:
                    product_id = item_data.get('item_id') if isinstance(item_data, dict) else int(item_key)
                    product = get_object_or_404(Product, pk=product_id)
                    quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                    line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    line_item.save()
                except Exception as e:
                    messages.error(request, f"Error processing item: {e}")
                    order.delete()
                    return redirect('view_bag')

            request.session['bag'] = {}
            return redirect('checkout_success', order_number=order.order_number)
    else:
        form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! Your order number is {order_number}.')
    return render(request, 'checkout/checkout_success.html', {'order': order})
