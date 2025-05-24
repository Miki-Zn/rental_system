import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()

@pytest.mark.django_db
def test_listings_list_api():
    client = APIClient()
    response = client.get('/api/listings/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_listing_create_api():
    user = User.objects.create_user(email='user@example.com', password='123')
    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "title": "New Apartment",
        "description": "Nice and clean",
        "price": 1000,
        "location": "Moscow",
        "number_of_rooms": 2,
        "property_type": "apartment"
    }

    response = client.post('/api/listings/', payload, format='json')
    assert response.status_code == 201
    assert Listing.objects.count() == 1
