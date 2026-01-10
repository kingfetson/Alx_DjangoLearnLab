from bookshelf.models import Book
Book.objects.all()

book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year

Output
python
Copy code
# ('1984', 'George Orwell', 1949)
