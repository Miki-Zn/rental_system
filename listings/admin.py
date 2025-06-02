from django.contrib import admin
from .models import Listing, Review

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'owner', 'location', 'price', 'property_type',
        'number_of_rooms', 'is_active', 'created_at', 'average_rating_display'
    )
    list_filter = ('is_active', 'property_type', 'location', 'created_at')
    search_fields = ('title', 'description', 'location', 'owner__email')
    readonly_fields = ('created_at',)

    def average_rating_display(self, obj):
        return obj.average_rating() or 'No ratings'
    average_rating_display.short_description = 'Average Rating'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__email', 'listing__title')
    readonly_fields = ('created_at',)
