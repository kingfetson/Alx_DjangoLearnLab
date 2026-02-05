# api/urls.py

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    # List all books with filtering, search, and ordering
    path("books/", BookListView.as_view(), name="book-list"),

    # Retrieve details of a single book
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),

    # Create a new book (authenticated only)
    path("books/create/", BookCreateView.as_view(), name="book-create"),

    # Update an existing book (authenticated only)
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),

    # Delete a book (authenticated only)
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
]
