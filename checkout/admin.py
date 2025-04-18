from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemInline,)
    readonly_fields = ('order_number', 'date', 'order_total',
                       'delivery_cost', 'grand_total',
                       'original_bag', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'address',
              'order_total', 'delivery_cost', 'grand_total',
              'original_bag', 'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost', 'grand_total')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
