from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from listings.models import Listing
from bookings.models import Booking
from rest_framework import status
from datetime import date, timedelta

class BookingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='pass1234')

        self.listing = Listing.objects.create(
            title="Test Listing",
            description="A nice place",
            price=100,
            owner=self.user,
            number_of_rooms=2,
            property_type="apartment"
        )

        self.create_url = reverse('booking-list')


        self.client.force_authenticate(user=self.user)

    def test_create_booking_success(self):
        data = {
            "listing": self.listing.id,
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=2)).isoformat(),
            "is_confirmed": False
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.listing, self.listing)
        self.assertEqual(booking.user, self.user)

    def test_create_booking_invalid_dates(self):
        data = {
            "listing": self.listing.id,
            "start_date": date.today().isoformat(),
            "end_date": (date.today() - timedelta(days=1)).isoformat(),
            "is_confirmed": False
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(
            response.data['non_field_errors'][0],
            'Start date must be before or equal to end date.'
        )

    def test_create_booking_overlapping_dates(self):
        Booking.objects.create(
            listing=self.listing,
            user=self.user,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
            is_confirmed=True
        )


        data = {
            "listing": self.listing.id,
            "start_date": date.today() + timedelta(days=3),
            "end_date": date.today() + timedelta(days=6),
            "is_confirmed": True
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
