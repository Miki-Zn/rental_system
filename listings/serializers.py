from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['owner', 'title', 'description', 'location', 'price', 'number_of_rooms', 'property_type', 'is_active', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def validate_owner(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Owner does not exist.")
        return value