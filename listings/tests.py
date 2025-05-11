import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from listings.models import Listing
from users.models import User

@pytest.fixture
def user():
    return User.objects.create_user(email='testuser@example.com', password='testpassword123')

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def listing(user):
    return Listing.objects.create(
        owner=user,
        title='Test Listing',
        description='A nice place to live',
        location='Berlin',
        price=500,
        rooms=2,
        property_type='apartment'
    )

def test_create_listing(auth_client):
    url = reverse('listing-list')
    data = {
        'title': 'New Listing',
        'description': 'Amazing apartment in Berlin!',
        'location': 'Berlin',
        'price': 1000,
        'rooms': 3,
        'property_type': 'apartment'
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Listing.objects.count() == 1

def test_list_listings(auth_client, listing):
    url = reverse('listing-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] == 1

def test_retrieve_listing(auth_client, listing):
    url = reverse('listing-detail', args=[listing.id])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['title'] == listing.title

def test_update_listing(auth_client, listing):
    url = reverse('listing-detail', args=[listing.id])
    data = {
        'title': 'Updated Title',
        'description': listing.description,
        'location': listing.location,
        'price': listing.price,
        'rooms': listing.rooms,
        'property_type': listing.property_type
    }
    response = auth_client.put(url, data, format='json')
    assert response.status_code == 200
    listing.refresh_from_db()
    assert listing.title == 'Updated Title'

def test_delete_listing(auth_client, listing):
    url = reverse('listing-detail', args=[listing.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert Listing.objects.count() == 0

def test_filter_by_price(auth_client, listing):
    url = reverse('listing-list')
    response = auth_client.get(url, {'min_price': 400, 'max_price': 600})
    assert response.status_code == 200
    assert response.data['count'] == 1

def test_filter_by_location(auth_client, listing):
    url = reverse('listing-list')
    response = auth_client.get(url, {'location': 'Berlin'})
    assert response.status_code == 200
    assert response.data['count'] == 1

def test_filter_by_rooms(auth_client, listing):
    url = reverse('listing-list')
    response = auth_client.get(url, {'min_rooms': 1, 'max_rooms': 3})
    assert response.status_code == 200
    assert response.data['count'] == 1

def test_search_in_title(auth_client, listing):
    url = reverse('listing-list')
    response = auth_client.get(url, {'search': 'Test'})
    assert response.status_code == 200
    assert response.data['count'] == 1

def test_order_by_price(auth_client, listing):
    Listing.objects.create(
        owner=listing.owner,
        title='Cheap Place',
        description='Cheap and cozy',
        location='Berlin',
        price=200,
        rooms=1,
        property_type='apartment'
    )
    url = reverse('listing-list')
    response = auth_client.get(url, {'ordering': 'price'})
    assert response.status_code == 200
    assert response.data['results'][0]['price'] == 200
