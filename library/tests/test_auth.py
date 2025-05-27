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


@pytest.mark.django_db
def test_register_with_existing_username():
    client = APIClient()
    User.objects.create_user(username="existinguser", password="pass123")

    # Trying to register with existing username should fail
    response = client.post("/api/auth/register/", {
        "username": "existinguser",
        "email": "other@example.com",
        "password": "AnotherPass123!"
    }, format='json')
    assert response.status_code == 400
    assert "username" in response.data


@pytest.mark.django_db
def test_login_with_wrong_password():
    client = APIClient()
    User.objects.create_user(username="user1", password="correctpass")

    # Login with wrong password should fail
    response = client.post("/api/auth/login/", {
        "username": "user1",
        "password": "wrongpass"
    }, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_with_nonexistent_user():
    client = APIClient()

    # Login with a user that doesn't exist should fail
    response = client.post("/api/auth/login/", {
        "username": "no_such_user",
        "password": "any_password"
    }, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_register_missing_fields():
    client = APIClient()

    # Missing password
    response = client.post("/api/auth/register/", {
        "username": "user2",
        "email": "user2@example.com"
    }, format='json')
    assert response.status_code == 400
    assert "password" in response.data

    # Missing username
    response = client.post("/api/auth/register/", {
        "email": "user3@example.com",
        "password": "StrongPass123!"
    }, format='json')
    assert response.status_code == 400
    assert "username" in response.data
