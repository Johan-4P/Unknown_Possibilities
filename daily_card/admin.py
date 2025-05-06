from django.contrib import admin
from .models import DailyCardDraw


@admin.register(DailyCardDraw)
class DailyCardDrawAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'drawn_at')
    list_filter = ('drawn_at',)
    search_fields = ('user__username', 'card__name')
    ordering = ('-drawn_at',)
