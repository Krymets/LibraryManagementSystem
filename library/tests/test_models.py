import pytest
from library.models import Book, User, Loan
from django.utils import timezone

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
