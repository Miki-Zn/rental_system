from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'listing', 'user', 'booking', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'listing']

    def validate(self, data):
        request = self.context.get('request')
        booking = data.get('booking')

        if not booking:
            raise serializers.ValidationError("Booking is required.")

        if booking.user != request.user:
            raise serializers.ValidationError("You can only review your own bookings.")

        if not booking.is_confirmed:
            raise serializers.ValidationError("You can only review confirmed bookings.")

        if hasattr(booking, 'review'):
            raise serializers.ValidationError("Review for this booking already exists.")

        return data
