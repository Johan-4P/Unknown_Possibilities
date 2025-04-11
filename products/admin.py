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


@admin.register(TarotCard)
class TarotCardAdmin(admin.ModelAdmin):
    """Admin settings for TarotCard model."""
    list_display = ('name', 'product', 'get_categories')
    list_filter = ('product', 'categories')
    search_fields = ('name', 'message')
    filter_horizontal = ('categories',)

    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_categories.short_description = 'Categories'

    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
