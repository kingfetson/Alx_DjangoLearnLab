from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# -------------------------------
# Book List View (READ-ONLY)
# -------------------------------
class BookListView(generics.ListAPIView):
    """
    Returns a list of all books.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------
# Book Detail View (READ-ONLY)
# -------------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    Returns a single book by ID.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------
# Book Create View (AUTH REQUIRED)
# -------------------------------
class BookCreateView(generics.CreateAPIView):
    """
    Allows authenticated users to create a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------------
# Book Update View (AUTH REQUIRED)
# -------------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    Allows authenticated users to update an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------------
# Book Delete View (AUTH REQUIRED)
# -------------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    Allows authenticated users to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
