from rest_framework import viewsets, permissions, generics, status, filters, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from typing import Any

from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer, RegisterSerializer


ROLE_DESCRIPTION = """
### User Roles & Permissions

| Role                  | Access to /api/books/ | Search Books | Borrow Books (/api/loans/) | Return Books (/api/return/<id>/) | Admin Panel Access |
|-----------------------|----------------------|--------------|---------------------------|---------------------------------|--------------------|
| Anonymous User         | ✅ View Only          | ✅           | ❌                         | ❌                               | ❌                  |
| Registered User        | ✅                    | ✅           | ✅ *(JWT required)*         | ✅ *(JWT required)*               | ❌                  |
| Administrator         | ✅                    | ✅           | ✅ *(JWT required)*         | ✅ *(JWT required)*               | ✅                  |

*JWT authentication is required for borrowing and returning books.
"""


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    serializer_class = RegisterSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    Supports filtering, searching and ordering.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'available']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'page_count']

    @swagger_auto_schema(operation_description=ROLE_DESCRIPTION)
    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        List all books with filtering, searching, and ordering options.
        """
        return super().list(request, *args, **kwargs)


class LoanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loans (borrowing books) to be viewed or created.
    Only authenticated users can create loans.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description=ROLE_DESCRIPTION)
    def create(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new loan (borrow a book).
        Validates that the book is available.
        """
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.ModelSerializer) -> None:
        """
        Override to update book availability when loan is created.
        """
        book = serializer.validated_data['book']
        if not book.available:
            raise serializers.ValidationError("Book is not available for borrowing.")
        book.available = False
        book.save()
        serializer.save(user=self.request.user)


class ReturnBookView(APIView):
    """
    API endpoint to return a borrowed book.
    Only authenticated users can return books they have borrowed.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description=ROLE_DESCRIPTION)
    def post(self, request: Any, pk: int) -> Response:
        """
        Mark a loan as returned, update book availability.

        Args:
            request: The HTTP request.
            pk: Primary key of the loan to be returned.

        Returns:
            A JSON response indicating success or failure.
        """
        try:
            loan = Loan.objects.get(pk=pk, user=request.user, returned_at__isnull=True)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found or already returned'}, status=status.HTTP_404_NOT_FOUND)

        loan.returned_at = timezone.now()
        loan.book.available = True
        loan.book.save()
        loan.save()
        return Response({'status': 'Book returned successfully'}, status=status.HTTP_200_OK)
