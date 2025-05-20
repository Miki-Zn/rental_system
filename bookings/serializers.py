from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.ReadOnlyField(source='listing.title')
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'user',
            'start_date', 'end_date',
            'is_confirmed', 'created_at'
        ]
        read_only_fields = ['user', 'created_at', 'is_confirmed', 'listing_title']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date must be before or equal to end date.")
        return data
