from django.urls import path
from .views import list_books
from .views import LibraryDetailView

from .views import register_view, login_view, logout_view

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view
    path('books/', list_books, name='list_books'),
    
    # Class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
