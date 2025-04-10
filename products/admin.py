from django.contrib import admin
from .models import Product, Category, TarotCard

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    """Admin settings for Product model."""
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'stock',
        'available',
        'created_at',
        'updated_at',
    )
    list_filter = ('category', 'available')
    search_fields = ('sku', 'name', 'description')
    ordering = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    """Admin settings for Category model."""
    list_display = ('friendly_name', 'name')
    search_fields = ('friendly_name', 'name')


class TarotCardAdmin(admin.ModelAdmin):
    """Admin settings for TarotCard model."""
    list_display = ('name', 'product', 'categories',)
    list_filter = ('product', 'categories')
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(TarotCard)