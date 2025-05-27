import pytest
from rest_framework.test import APIClient
from library.models import User, Book


@pytest.mark.django_db
def test_borrow_and_return_book():
    client = APIClient()

    # Create a test user and a book
    user = User.objects.create_user(username="loanuser", password="pass123")
    book = Book.objects.create(title="Loan Book", author="Author", isbn="1111111111111", page_count=100)

    client.force_authenticate(user=user)

    # Borrow the book (POST /api/loans/)
    borrow_response = client.post("/api/loans/", {"book": book.id}, format='json')
    assert borrow_response.status_code == 201
    loan_id = borrow_response.data["id"]

    # The book should now be unavailable
    book.refresh_from_db()
    assert book.available is False

    # Attempting to borrow the same book again should fail with 400
    second_borrow = client.post("/api/loans/", {"book": book.id}, format='json')
    assert second_borrow.status_code == 400

    # Return the book (POST /api/return/<loan_id>/)
    return_response = client.post(f"/api/return/{loan_id}/", format='json')
    assert return_response.status_code == 200
    assert return_response.data["status"] == "Book returned successfully"

    # The book should be available again
    book.refresh_from_db()
    assert book.available is True

    # Trying to return the book again should return 404 as it is already returned
    second_return = client.post(f"/api/return/{loan_id}/", format='json')
    assert second_return.status_code == 404


@pytest.mark.django_db
def test_loan_access_control():
    client = APIClient()

    # Create two users and a book
    user1 = User.objects.create_user(username="user1", password="pass1")
    user2 = User.objects.create_user(username="user2", password="pass2")
    book = Book.objects.create(title="Access Book", author="Author", isbn="2222222222222", page_count=50)

    # user1 borrows the book
    client.force_authenticate(user=user1)
    borrow_response = client.post("/api/loans/", {"book": book.id}, format='json')
    loan_id = borrow_response.data["id"]

    # user2 tries to return user1's borrowed book - should return 404
    client.force_authenticate(user=user2)
    return_response = client.post(f"/api/return/{loan_id}/", format='json')
    assert return_response.status_code == 404
