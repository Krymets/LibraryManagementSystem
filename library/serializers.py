from rest_framework import serializers
from .models import Book, Loan, User
from django.contrib.auth.password_validation import validate_password
from typing import Any, Dict


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, exposing id, username, and email fields.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Validates password using Django's password validators.
    Accepts username, email, and password fields.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text="User password (write-only)."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Create a new user instance with hashed password.

        Args:
            validated_data (dict): Validated data containing username, email, and password.

        Returns:
            User: The newly created user instance.
        """
        user = User.objects.create_user(**validated_data)
        return user


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Serializes all fields of the Book model.
    """
    class Meta:
        model = Book
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Loan model.

    Serializes all fields of the Loan model.
    """
    class Meta:
        model = Loan
        fields = '__all__'
