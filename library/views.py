from rest_framework import viewsets, permissions, generics, status, filters, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'availability']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'page_count']


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if not book.available:
            raise serializers.ValidationError("Book is not available for borrowing.")
        # Update book availability
        book.available = False
        book.save()
        # Create the loan
        serializer.save(user=self.request.user)


class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            loan = Loan.objects.get(pk=pk, user=request.user, returned_at__isnull=True)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found or already returned'}, status=status.HTTP_404_NOT_FOUND)

        loan.returned_at = timezone.now()
        loan.book.available = True
        loan.book.save()
        loan.save()
        return Response({'status': 'Book returned successfully'}, status=status.HTTP_200_OK)
