from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class BookListCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password="testpassword", email="zTqFP@example.com"
        )
        self.url = reverse("books:book-list-create")
        self.book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            published_date="2021-01-01",
            isbn="789",
            language="English",
            added_by=self.user,
        )
        self.book2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            published_date="2022-01-01",
            isbn="123",
            language="Spanish",
            added_by=self.user,
        )
        self.book3 = Book.objects.create(
            title="Book 3",
            author="Author 1",
            published_date="2023-01-01",
            isbn="456",
            language="English",
            added_by=self.user,
        )

    def test_filter_by_author(self):
        response = self.client.get(self.url, {"author": "Author 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "Book 1")
        self.assertEqual(response.data["results"][1]["title"], "Book 3")

    def test_filter_by_published_date(self):
        response = self.client.get(self.url, {"published_date": "2022"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Book 2")

    def test_filter_by_language(self):
        response = self.client.get(self.url, {"language": "English"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "Book 1")
        self.assertEqual(response.data["results"][1]["title"], "Book 3")

    def test_filter_by_multiple_fields(self):
        response = self.client.get(
            self.url, {"author": "Author 1", "language": "English"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "Book 1")
        self.assertEqual(response.data["results"][1]["title"], "Book 3")

    def test_create_book_authenticated(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2022-01-01",
            "isbn": "1234567890123",
            "pages": 300,
            "cover": "http://example.com/cover.jpg",
            "language": "English",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2022-01-01",
            "isbn": "1234567890123",
            "pages": 300,
            "cover": "http://example.com/cover.jpg",
            "language": "English",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookRetrieveUpdateDeleteViewTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com", password="ownerpassword"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="otherpassword"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date="2022-01-01",
            isbn="1234567890123",
            pages=300,
            cover="http://example.com/cover.jpg",
            language="English",
            added_by=self.owner,
        )
        self.book_url = reverse("books:book-detail", args=[self.book.pk])

    def test_retrieve_book_authenticated(self):
        refresh = RefreshToken.for_user(User.objects.get(email="owner@example.com"))
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    def test_retrieve_book_unauthenticated(self):
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book_authenticated_as_owner(self):
        refresh = RefreshToken.for_user(User.objects.get(email="owner@example.com"))
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {
            "title": "Updated Test Book",
            "author": "Updated Author",
            "published_date": "2022-02-01",
            "isbn": "9876543210123",
            "pages": 400,
            "cover": "http://example.com/updated_cover.jpg",
            "language": "Spanish",
        }
        response = self.client.put(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Test Book")

    def test_update_book_authenticated_as_other_user(self):
        refresh = RefreshToken.for_user(User.objects.get(email="other@example.com"))
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {
            "title": "Should Not Update",
            "author": "Not Allowed",
        }
        response = self.client.put(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated_as_owner(self):
        refresh = RefreshToken.for_user(User.objects.get(email="owner@example.com"))
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_delete_book_authenticated_as_other_user(self):
        refresh = RefreshToken.for_user(User.objects.get(email="other@example.com"))
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
