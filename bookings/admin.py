from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'listing', 'user', 'start_date', 'end_date',
        'is_confirmed', 'created_at'
    )
    list_filter = ('is_confirmed', 'start_date', 'end_date', 'created_at')
    search_fields = (
        'listing__title',
        'user__username',
        'user__email'
    )
    readonly_fields = ('created_at',)
