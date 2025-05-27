import pytest
from rest_framework.test import APIClient
from library.models import User

@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()

    # Registration
    response = client.post("/api/auth/register/", {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "VeryStrongPass123!"
    }, format='json')
    assert response.status_code == 201
    assert User.objects.filter(username="newuser").exists()

    # Login (Get JWT)
    response = client.post("/api/auth/login/", {
        "username": "newuser",
        "password": "VeryStrongPass123!"
    }, format='json')
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
