from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters

from books.filters import BookFilter
from books.models import Book
from books.serializers import BookSerializer
from books.pagination import BookPagination
from books.permissions import IsOwnerOrReadOnly


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
