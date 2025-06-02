from django.contrib import admin
from .models import SearchHistory, ViewHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'keyword', 'searched_at')
    search_fields = ('keyword', 'user__username', 'user__email')
    list_filter = ('searched_at',)
    ordering = ('-searched_at',)

    def user_display(self, obj):
        return obj.user.username if obj.user else "Anonymous"
    user_display.short_description = 'User'


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'listing', 'viewed_at')
    search_fields = ('listing__title', 'user__username', 'user__email')
    list_filter = ('viewed_at', 'listing')
    ordering = ('-viewed_at',)

    def user_display(self, obj):
        return obj.user.username if obj.user else "Anonymous"
    user_display.short_description = 'User'
