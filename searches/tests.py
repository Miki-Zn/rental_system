import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from searches.models import SearchHistory

@pytest.fixture
def user():
    return User.objects.create_user(email='testuser@example.com', password='testpassword123')

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

def test_create_search_history(auth_client):
    url = reverse('search-history-create')
    data = {'keyword': 'Berlin Apartment'}
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 201
    assert SearchHistory.objects.count() == 1

def test_get_popular_searches(auth_client):
    SearchHistory.objects.create(user=auth_client.handler._force_user, keyword='Berlin')
    SearchHistory.objects.create(user=auth_client.handler._force_user, keyword='Munich')
    SearchHistory.objects.create(user=auth_client.handler._force_user, keyword='Berlin')

    url = reverse('popular-searches')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data[0]['keyword'] == 'Berlin'
