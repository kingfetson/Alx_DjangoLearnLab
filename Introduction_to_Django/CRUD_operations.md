# CRUD Operations for Book Model

This document records the Create, Retrieve, Update, and Delete (CRUD) operations
performed on the `Book` model using the Django shell.

---

## Create Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
book
