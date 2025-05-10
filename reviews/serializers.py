from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'listing', 'user', 'booking', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        if 'booking' not in data:
            raise serializers.ValidationError("Booking is required")
        if not data['booking'].is_confirmed:
            raise serializers.ValidationError("Booking is not confirmed.")
        return data
