import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from searches.models import SearchHistory

@pytest.mark.django_db
def test_create_and_list_search_history():
    user = User.objects.create_user(email='test@example.com', password='pass1234')
    client = APIClient()
    client.force_authenticate(user=user)


    response = client.post(reverse('search-history-create'), {'keyword': 'apartment'})
    assert response.status_code == 201
    assert SearchHistory.objects.count() == 1
    assert SearchHistory.objects.first().keyword == 'apartment'
    assert SearchHistory.objects.first().user == user


