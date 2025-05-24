import datetime
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from bookings.models import Booking
from listings.models import Listing
from users.models import User
from reviews.models import Review

@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@example.com", password="password123")

@pytest.fixture
def listing(db, user):
    return Listing.objects.create(
        owner=user,
        title="Test Listing",
        description="A test listing",
        location="Test Location",
        price=100,
        number_of_rooms=2,
        property_type="Apartment",
        is_active=True,
    )

@pytest.fixture
def booking(db, user, listing):
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=3)
    return Booking.objects.create(
        user=user,
        listing=listing,
        start_date=start_date,
        end_date=end_date,
        is_confirmed=True,
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_create_review(api_client, user, booking, listing):
    api_client.force_authenticate(user=user)
    url = reverse('reviews:reviews-list')
    data = {
        "booking": booking.id,
        "listing": listing.id,
        "rating": 5,
        "comment": "Great place!",
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Review.objects.filter(booking=booking, user=user, listing=listing).exists()

@pytest.mark.django_db
def test_list_reviews(api_client, listing, user, booking):
    Review.objects.create(
        booking=booking,
        user=user,
        listing=listing,
        rating=4,
        comment="Nice stay"
    )
    url = reverse('reviews:reviews-list') + f'?listing={listing.id}'
    response = api_client.get(url)
    assert response.status_code == 200
    data_list = response.data if isinstance(response.data, list) else response.data.get('results', [])
    assert len(data_list) > 0
    assert data_list[0]['comment'] == "Nice stay"

