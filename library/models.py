from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from typing import Optional


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        is_admin (bool): Indicates whether the user has administrator privileges.
    """
    is_admin: models.BooleanField = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_admin:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)


class Book(models.Model):
    """
    Model representing a book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The unique ISBN number of the book.
        page_count (int): The total number of pages in the book.
        available (bool): Availability status of the book for borrowing.
    """

    title: models.CharField = models.CharField(max_length=255)
    author: models.CharField = models.CharField(max_length=255)
    isbn: models.CharField = models.CharField(max_length=13, unique=True)
    page_count: models.PositiveIntegerField = models.PositiveIntegerField()
    available: models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the book, which is its title.

        Returns:
            str: Title of the book.
        """
        return f"{self.title} by {self.author}"


class Loan(models.Model):
    """
    Model representing a loan of a book to a user.

    Attributes:
        user (User): The user who borrowed the book.
        book (Book): The book that was borrowed.
        borrowed_at (datetime): Timestamp when the book was borrowed.
        returned_at (Optional[datetime]): Timestamp when the book was returned; None if not returned.
    """

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    book: models.ForeignKey = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at: models.DateTimeField = models.DateTimeField(default=timezone.now)
    returned_at: Optional[models.DateTimeField] = models.DateTimeField(null=True, blank=True)

    def is_returned(self) -> bool:
        """
        Checks if the loaned book has been returned.

        Returns:
            bool: True if the book has been returned, False otherwise.
        """
        return self.returned_at is not None

    def __str__(self) -> str:
        return f"Loan of '{self.book.title}' by {self.user.username}"

    def clean(self):
        if not self.book.available:
            raise ValidationError("Cannot loan a book that is not available.")
