from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'user_display', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'listing')
    search_fields = ('listing__title', 'user__username', 'comment')
    ordering = ('-created_at',)

    def user_display(self, obj):
        return obj.user.username if obj.user else "Anonymous"
    user_display.short_description = 'User'
