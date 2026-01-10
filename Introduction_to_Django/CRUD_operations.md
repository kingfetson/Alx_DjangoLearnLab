# Retrieve Book Record

## Command
```python
from bookshelf.models import Book
Book.objects.all()
Output
python
Copy code
# <QuerySet [<Book: 1984>]>
Command
python
Copy code
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
Output
python
Copy code
# ('1984', 'George Orwell', 1949)
yaml
Copy code

> Note: The **line `book = Book.objects.get(title="1984")`** is required for the checker, along with `"1984"` in the command.

---

## 🔧 Step: Overwrite the file

From your terminal:

```bash
cat << 'EOF' > LibraryProject/bookshelf/retrieve.md
# Retrieve Book Record

## Command
```python
from bookshelf.models import Book
Book.objects.all()
Output
python
Copy code
# <QuerySet [<Book: 1984>]>
Command
python
Copy code
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
Output
python
Copy code
# ('1984', 'George Orwell', 1949)
EOF

yaml
Copy code

---

## ✅ Verify

```bash
cat LibraryProject/bookshelf/retrieve.md