from django.contrib import admin
from .models import UserProfile
from checkout.models import Order

class OrderInline(admin.TabularInline):
    model = Order
    fields = ('order_number', 'full_name', 'email', 'grand_total', 'date')
    readonly_fields = fields
    extra = 0
    can_delete = False

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'country', 'town_or_city')

    inlines = (OrderInline,)
