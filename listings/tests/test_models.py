import pytest
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()

@pytest.mark.django_db
def test_listing_creation():
    user = User.objects.create_user(email='user@example.com', password='123')
    listing = Listing.objects.create(
        title='Cozy Apartment',
        description='Great place in the center',
        price=1500,
        location='Moscow',
        number_of_rooms=2,
        property_type='apartment',
        owner=user
    )
    assert listing.title == 'Cozy Apartment'
    assert listing.owner == user
