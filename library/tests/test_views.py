import pytest
from rest_framework.test import APIClient
from library.models import User, Book

@pytest.mark.django_db
def test_book_list_and_create():
    client = APIClient()
    # Create a test user and log in
    user = User.objects.create_user(username="user1", password="pass")
    client.force_authenticate(user=user)

    # List of books (GET)
    response = client.get("/api/books/")
    assert response.status_code == 200

    # Creating a book (POST)
    data = {"title": "New Book", "author": "Author", "isbn": "1234567890125", "page_count": 150}
    response = client.post("/api/books/", data, format='json')
    assert response.status_code == 201
    assert response.data['title'] == "New Book"
