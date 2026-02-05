"""
API Views for Book Management with Advanced Query Capabilities

This module provides API endpoints for managing books with support for:
- Filtering by title, author, and publication_year
- Searching across title and author fields
- Ordering by any field (especially title and publication_year)
"""

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer


# -------------------------------
# Book List View with Advanced Query Capabilities
# -------------------------------
class BookListView(generics.ListAPIView):
    """
    Lists all books with advanced query capabilities.
    
    Features:
    - Filtering: Filter by title, author, publication_year
    - Searching: Search in title and author fields
    - Ordering: Order by any field (default: title, publication_year)
    
    Permission: Read-only for unauthenticated users, read/write for authenticated users.
    
    Example Usage:
    - Filter by author: /api/books/?author__name=John Doe
    - Filter by year: /api/books/?publication_year=2023
    - Search: /api/books/?search=django
    - Order by title: /api/books/?ordering=title
    - Order by year (descending): /api/books/?ordering=-publication_year
    - Combined: /api/books/?author__name=John&search=python&ordering=title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering configuration
    filterset_fields = ['title', 'author__name', 'publication_year']
    
    # Search configuration - allows text search across these fields
    search_fields = ['title', 'author__name']
    
    # Ordering configuration - allows sorting by these fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by ID.
    
    Permission: Read-only for unauthenticated users, read/write for authenticated users.
    
    Example Usage:
    - GET /api/books/1/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book.
    
    Permission: Authenticated users only.
    
    Example Usage:
    - POST /api/books/create/
    Body: {"title": "New Book", "author": 1, "publication_year": 2024}
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book (full or partial update).
    
    Permission: Authenticated users only.
    
    Example Usage:
    - PUT /api/books/1/update/
    - PATCH /api/books/1/update/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a book.
    
    Permission: Authenticated users only.
    
    Example Usage:
    - DELETE /api/books/1/delete/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]