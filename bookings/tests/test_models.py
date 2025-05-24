import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from bookings.models import Booking
from listings.models import Listing
from users.models import User

@pytest.mark.django_db
class TestBookingModel:

    def setup_method(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123'
        )
        self.listing = Listing.objects.create(
            owner=self.user,
            title='Test Listing',
            description='Test Desc',
            location='Test City',
            price=100.00,
            number_of_rooms=2,
            property_type='apartment',
            is_active=True
        )

    def test_valid_booking_creation(self):
        booking = Booking(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() + timedelta(days=1),
            end_date=timezone.now().date() + timedelta(days=3),
            is_confirmed=True,
        )
        booking.full_clean()
        booking.save()
        assert Booking.objects.count() == 1

    def test_start_date_after_end_date_raises_validation_error(self):
        booking = Booking(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() + timedelta(days=5),
            end_date=timezone.now().date() + timedelta(days=3),
            is_confirmed=True,
        )
        with pytest.raises(ValidationError) as e:
            booking.full_clean()
        assert 'Start date must be before end date.' in str(e.value)

    def test_overlapping_confirmed_booking_raises_validation_error(self):
        Booking.objects.create(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() + timedelta(days=1),
            end_date=timezone.now().date() + timedelta(days=5),
            is_confirmed=True,
        )
        new_booking = Booking(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() + timedelta(days=3),
            end_date=timezone.now().date() + timedelta(days=6),
            is_confirmed=True,
        )
        with pytest.raises(ValidationError) as e:
            new_booking.full_clean()
        assert 'This listing is already booked for the selected dates.' in str(e.value)

    def test_overlapping_unconfirmed_booking_allowed(self):
        Booking.objects.create(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() + timedelta(days=1),
            end_date=timezone.now().date() + timedelta(days=5),
            is_confirmed=False,
        )
        new_booking = Booking(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() + timedelta(days=3),
            end_date=timezone.now().date() + timedelta(days=6),
            is_confirmed=True,
        )
        new_booking.full_clean()
        new_booking.save()
        assert Booking.objects.count() == 2
