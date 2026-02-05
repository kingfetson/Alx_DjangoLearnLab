# api/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        
        # Create an author
        self.author = Author.objects.create(name="John Doe")
        
        # Create books
        self.book1 = Book.objects.create(title="Django Basics", author=self.author, publication_year=2023)
        self.book2 = Book.objects.create(title="Advanced Django", author=self.author, publication_year=2022)
        self.book3 = Book.objects.create(title="Python Tricks", author=self.author, publication_year=2023)

        # API client
        self.client = APIClient()
        
        # URLs
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.update_url = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.delete_url = lambda pk: reverse("book-delete", kwargs={"pk": pk})

    # ----------------------
    # READ / LIST TESTS
    # ----------------------
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_books_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=2023")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Python Tricks")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Python Tricks")

    def test_order_books_by_title(self):
        response = self.client.get(f"{self.list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Ensure ordering by title

    # ----------------------
    # CREATE TESTS
    # ----------------------
    def test_create_book_requires_authentication(self):
        # Unauthenticated request
        response = self.client.post(self.create_url, {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2024
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated request
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.create_url, {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2024
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    # ----------------------
    # UPDATE TESTS
    # ----------------------
    def test_update_book_unauthenticated(self):
        response = self.client.put(self.update_url(self.book1.id), {
            "title": "Updated Title",
            "author": self.author.id,
            "publication_year": 2023
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated update
        self.client.login(username="testuser", password="password123")
        response = self.client.put(self.update_url(self.book1.id), {
            "title": "Updated Title",
            "author": self.author.id,
            "publication_year": 2023
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # ----------------------
    # DELETE TESTS
    # ----------------------
    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated delete
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
