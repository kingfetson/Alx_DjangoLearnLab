from django.urls import path
from .views import list_books
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view
    path('books/', list_books, name='list_books'),
    
    # Class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
