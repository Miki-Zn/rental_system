import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email='user@example.com', password='password123')
    assert user.email == 'user@example.com'
    assert user.check_password('password123')
    assert user.role == 'user'
    assert not user.is_staff
    assert not user.is_superuser

@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(email='admin@example.com', password='adminpass')
    assert admin.email == 'admin@example.com'
    assert admin.check_password('adminpass')
    assert admin.role == 'admin'
    assert admin.is_staff
    assert admin.is_superuser

@pytest.mark.django_db
def test_user_str():
    user = User.objects.create_user(email='testuser@example.com', password='testpass')
    assert str(user) == 'testuser@example.com'

@pytest.mark.django_db
def test_create_user_without_email_should_raise_error():
    with pytest.raises(ValueError):
        User.objects.create_user(email='', password='nopass')

@pytest.mark.django_db
def test_login_with_correct_credentials():
    user = User.objects.create_user(email='loginuser@example.com', password='loginpass')
    client = APIClient()
    response = client.post(
        reverse('token_obtain_pair'),
        {'email': 'loginuser@example.com', 'password': 'loginpass'},
        format='json'
    )
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_login_with_wrong_credentials():
    user = User.objects.create_user(email='wronglogin@example.com', password='correctpass')
    client = APIClient()
    response = client.post(
        reverse('token_obtain_pair'),
        {'email': 'wronglogin@example.com', 'password': 'wrongpass'},
        format='json'
    )
    assert response.status_code == 401 or response.status_code == 400

