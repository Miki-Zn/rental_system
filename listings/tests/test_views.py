import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()

@pytest.mark.django_db
def test_listing_create_view(client):
    user = User.objects.create_user(email='user@example.com', password='123')
    client.login(username='user@example.com', password='123')

    url = reverse('listings:listing_create')
    data = {
        'title': 'Test Flat',
        'description': 'Some info',
        'price': 1000,
        'location': 'Kazan',
        'number_of_rooms': 1,
        'property_type': 'apartment'
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert Listing.objects.count() == 1
