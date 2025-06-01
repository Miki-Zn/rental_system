from rest_framework import serializers
from django.utils import timezone
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
        request = self.context.get('request')
        user = request.user if request else None

        start_date = data.get('start_date') or getattr(self.instance, 'start_date', None)
        end_date = data.get('end_date') or getattr(self.instance, 'end_date', None)
        listing = data.get('listing') or getattr(self.instance, 'listing', None)

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                'non_field_errors': ['Start date must be before or equal to end date.']
            })


        if start_date and start_date < timezone.now().date():
            raise serializers.ValidationError({
                'start_date': ['Start date cannot be in the past.']
            })


        if listing and user and listing.owner == user:
            raise serializers.ValidationError({
                'listing': ['You cannot book your own listing.']
            })


        if listing and start_date and end_date:
            overlapping = Booking.objects.filter(
                listing=listing,
                is_confirmed=True,
                end_date__gte=start_date,
                start_date__lte=end_date,
            )
            if self.instance:
                overlapping = overlapping.exclude(pk=self.instance.pk)

            if overlapping.exists():
                raise serializers.ValidationError({
                    'non_field_errors': ['This listing is already booked for the selected dates.']
                })

        return data
