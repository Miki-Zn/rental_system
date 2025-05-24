import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_login_with_wrong_credentials():
    User.objects.create_user(email="user@example.com", password="CorrectPass123")
    client = APIClient()

    response = client.post("/auth/jwt/create/", {
        "email": "user@example.com",
        "password": "WrongPass456"
    })

    assert response.status_code == 401
    assert "access" not in response.data


@pytest.mark.django_db
def test_update_user_profile():
    user = User.objects.create_user(email="test@example.com", password="Testpass123")
    client = APIClient()


    token_response = client.post("/auth/jwt/create/", {
        "email": "test@example.com",
        "password": "Testpass123"
    })
    access = token_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")


    response = client.put("/api/users/me/", {
        "email": user.email,
        "first_name": "Updated",
        "last_name": "User"
    }, format="json")

    print("Status code:", response.status_code)
    print("Response data:", response.data)

    assert response.status_code == 200
    assert response.data["first_name"] == "Updated"


@pytest.mark.django_db
def test_change_password_with_wrong_old_password():
    user = User.objects.create_user(email="test2@example.com", password="OldPass123")
    client = APIClient()

    token_response = client.post("/auth/jwt/create/", {
        "email": "test2@example.com",
        "password": "OldPass123"
    })
    access = token_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = client.post("/auth/users/set_password/", {
        "current_password": "WrongOldPass",
        "new_password": "NewSecurePass123"
    }, format="json")

    assert response.status_code == 400
    assert "current_password" in response.data


@pytest.mark.django_db
def test_token_refresh():
    user = User.objects.create_user(email="refresh@example.com", password="Pass1234")
    client = APIClient()

    login_response = client.post("/auth/jwt/create/", {
        "email": "refresh@example.com",
        "password": "Pass1234"
    })

    refresh = login_response.data["refresh"]

    refresh_response = client.post("/auth/jwt/refresh/", {
        "refresh": refresh
    })

    assert refresh_response.status_code == 200
    assert "access" in refresh_response.data
