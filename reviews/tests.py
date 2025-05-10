from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from listings.models import Listing
from bookings.models import Booking

class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            role="user"
        )

        self.listing = Listing.objects.create(
            title="Test Listing",
            description="A wonderful place to stay",
            price=100,
            number_of_rooms=3,
            location="Berlin",
            property_type="apartment",
            owner=self.user
        )

        self.booking = Booking.objects.create(
            user=self.user,
            listing=self.listing,
            start_date="2025-06-01",
            end_date="2025-06-10",
            is_confirmed=True
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_review(self):
        url = reverse('reviews:create')
        data = {
            "listing": self.listing.id,
            "rating": 5,
            "comment": "Excellent place to stay!",
            "booking": self.booking.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['comment'], "Excellent place to stay!")

    def test_review_creation_without_booking(self):
        url = reverse('reviews:create')
        data = {
            "listing": self.listing.id,
            "rating": 4,
            "comment": "Not bad, but could be better."
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Booking is required', response.data['non_field_errors'][0])

