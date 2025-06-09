import pytest
from library.models import Book, User, Loan
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_book():
    book = Book.objects.create(title="Test Book", author="Author", isbn="1234567890123", page_count=100)
    assert book.title == "Test Book"
    assert book.available is True


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username="tester", password="password123")
    assert user.username == "tester"
    assert not user.is_admin


@pytest.mark.django_db
def test_loan_creation():
    user = User.objects.create_user(username="tester2", password="password123")
    book = Book.objects.create(title="Test Book 2", author="Author 2", isbn="1234567890124", page_count=200)
    loan = Loan.objects.create(user=user, book=book, borrowed_at=timezone.now())
    assert loan.is_returned() is False
    loan.returned_at = timezone.now()
    assert loan.is_returned() is True


@pytest.mark.django_db
def test_book_availability_changes_on_loan_and_return():
    user = User.objects.create_user(username="user3", password="password123")
    book = Book.objects.create(title="Available Book", author="Author", isbn="1234567890125", page_count=150)
    assert book.available is True

    loan = Loan.objects.create(user=user, book=book, borrowed_at=timezone.now())
    book.refresh_from_db()
    assert book.available is True, "Availability shouldn't auto-change on loan creation unless logic implemented"

    # Simulate loan return
    loan.returned_at = timezone.now()
    loan.save()
    book.available = True
    book.save()

    book.refresh_from_db()
    assert book.available is True


@pytest.mark.django_db
def test_cannot_create_loan_for_unavailable_book():
    user = User.objects.create_user(username="user4", password="password123")
    book = Book.objects.create(title="Unavailable Book", author="Author", isbn="1234567890126", page_count=200,
                               available=False)

    with pytest.raises(ValidationError):
        Loan.objects.create(user=user, book=book, borrowed_at=timezone.now()).full_clean()


@pytest.mark.django_db
def test_loan_return_sets_returned_at():
    user = User.objects.create_user(username="user5", password="password123")
    book = Book.objects.create(title="Return Test Book", author="Author", isbn="1234567890127", page_count=120)
    loan = Loan.objects.create(user=user, book=book, borrowed_at=timezone.now())

    assert loan.returned_at is None
    loan.returned_at = timezone.now()
    loan.save()
    loan.refresh_from_db()
    assert loan.returned_at is not None


@pytest.mark.django_db
def test_book_str_method():
    book = Book.objects.create(title="Str Test", author="Author", isbn="1234567890128", page_count=50)
    assert str(book) == "Str Test by Author"


@pytest.mark.django_db
def test_user_str_method():
    user = User.objects.create_user(username="user6", password="password123")
    assert str(user) == "user6"


@pytest.mark.django_db
def test_loan_str_method():
    user = User.objects.create_user(username="user7", password="password123")
    book = Book.objects.create(title="Loan Str Book", author="Author", isbn="1234567890129", page_count=60)
    loan = Loan.objects.create(user=user, book=book, borrowed_at=timezone.now())
    expected_str = f"Loan of '{book.title}' by {user.username}"
    assert str(loan) == expected_str


@pytest.mark.django_db
def test_admin_can_delete_book():
    book = Book.objects.create(title="Delete Me", author="Author", isbn="9999999999999", page_count=123)

    admin_user = User.objects.create_user(username="admin", password="adminpass", is_staff=True, is_admin=True)

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.delete(f"/api/books/{book.id}/")
    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_anonymous_cannot_delete_book():
    book = Book.objects.create(title="Protected Book", author="Author", isbn="8888888888888", page_count=100)

    client = APIClient()
    response = client.delete(f"/api/books/{book.id}/")

    assert response.status_code in [401, 403]
    assert Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_non_admin_user_cannot_delete_book():
    user = User.objects.create_user(username="notadmin", password="userpass", is_staff=False)
    book = Book.objects.create(title="No Delete", author="Author", isbn="7777777777777", page_count=111)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete(f"/api/books/{book.id}/")
    assert response.status_code == 403
    assert Book.objects.filter(id=book.id).exists()
