from rest_framework import serializers
from .models import SearchHistory, ViewHistory

class PopularSearchSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    count = serializers.IntegerField()

class PopularListingSerializer(serializers.Serializer):
    listing = serializers.PrimaryKeyRelatedField(read_only=True)
    count = serializers.IntegerField()
