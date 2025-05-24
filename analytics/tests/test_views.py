from django.test import TestCase
from django.contrib.auth import get_user_model
from listings.models import Listing
from analytics.models import SearchHistory, ViewHistory
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()

def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    self.listing = Listing.objects.create(
        owner=self.user,
        title='Test Listing',
        description='Test description',
        location='Test City',
        price=100,
        number_of_rooms=2,
        property_type='apartment',
        is_active=True,
    )

    for _ in range(5):
        SearchHistory.objects.create(keyword='bitcoin')
    for _ in range(3):
        SearchHistory.objects.create(keyword='ethereum')

    for _ in range(7):
        ViewHistory.objects.create(listing=self.listing)

    def test_popular_searches(self):
        url = reverse('popular-searches')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)

    def test_popular_listings(self):
        url = reverse('popular-listings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
