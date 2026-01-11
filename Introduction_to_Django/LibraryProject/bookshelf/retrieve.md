
````md
# Retrieve Book Record

## Command
```python
from bookshelf.models import Book
Book.objects.all()
````

## Output

```python
# <QuerySet [<Book: 1984>]>
```

## Command

```python
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
```

## Output

```python
# ('1984', 'George Orwell', 1949)
