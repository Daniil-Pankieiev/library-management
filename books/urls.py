from django.urls import path
from books.views import BookListCreateView, BookRetrieveUpdateDeleteView

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookRetrieveUpdateDeleteView.as_view(), name="book-detail"),
]

app_name = "books"
