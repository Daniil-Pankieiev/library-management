from django_filters import rest_framework as filters
from books.models import Book


class BookFilter(filters.FilterSet):
    author = filters.CharFilter(lookup_expr="icontains")
    published_date = filters.CharFilter(field_name="published_date", lookup_expr="year")
    language = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Book
        fields = ["author", "published_date", "language"]
