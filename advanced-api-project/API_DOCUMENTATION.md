# 📚 Book API Documentation

**Base URL:** `http://localhost:8000/api/books/`  
**Content-Type:** `application/json`  
**Authentication:** Required for create, update, delete operations.  

---

## 1. List All Books

| Method | Endpoint | Description | Query Parameters | Example Request | Example Response |
|--------|----------|-------------|-----------------|----------------|-----------------|
| GET | `/api/books/` | List all books with filtering, searching, and ordering | `title`, `author__name`, `publication_year`, `search`, `ordering` | `/api/books/?author__name=John&search=django&ordering=-publication_year` | ```json [{"id":1,"title":"Django for Beginners","author":1,"publication_year":2023},{"id":2,"title":"Advanced Python","author":2,"publication_year":2022}]``` |

**Notes:**  
- `search` works on `title` and `author__name`  
- `ordering` can be any field; prefix with `-` for descending  

---

## 2. Retrieve Book Details

| Method | Endpoint | Description | Example Request | Example Response |
|--------|----------|-------------|----------------|-----------------|
| GET | `/api/books/<int:pk>/` | Retrieve details of a single book by ID | `/api/books/1/` | ```json {"id":1,"title":"Django for Beginners","author":1,"publication_year":2023}``` |

---

## 3. Create a Book

| Method | Endpoint | Description | Request Body | Example Response | Permissions |
|--------|----------|-------------|--------------|-----------------|------------|
| POST | `/api/books/create/` | Create a new book | ```json {"title":"New Book","author":1,"publication_year":2024}``` | ```json {"id":5,"title":"New Book","author":1,"publication_year":2024}``` | Authenticated users only |

---

## 4. Update a Book

| Method | Endpoint | Description | Request Body | Example Response | Permissions |
|--------|----------|-------------|--------------|-----------------|------------|
| PUT / PATCH | `/api/books/<int:pk>/update/` | Update an existing book (full or partial) | Full: ```json {"title":"Updated Book","author":2,"publication_year":2025}``` Partial (PATCH): ```json {"title":"Partially Updated Title"}``` | Updated book object | Authenticated users only |

---

## 5. Delete a Book

| Method | Endpoint | Description | Example Request | Example Response | Permissions |
|--------|----------|-------------|----------------|-----------------|------------|
| DELETE | `/api/books/<int:pk>/delete/` | Delete a book by ID | `/api/books/1/delete/` | `204 No Content` | Authenticated users only |

---

## 6. Filtering, Searching, Ordering Examples

| Feature | Example | Description |
|---------|---------|------------|
| Filter by publication year | `/api/books/?publication_year=2023` | Returns books published in 2023 |
| Filter by author | `/api/books/?author__name=John Doe` | Returns books authored by John Doe |
| Search | `/api/books/?search=django` | Returns books where "django" appears in title or author |
| Ordering ascending | `/api/books/?ordering=title` | Orders books by title ascending |
| Ordering descending | `/api/books/?ordering=-publication_year` | Orders books by publication year descending |
| Combined | `/api/books/?author__name=John&search=python&ordering=title` | Filter, search, and order in one request |

---

# ⚡ Quick CRUD Workflow & Permissions

| Action | Endpoint | Method | Auth Required | Notes |
|--------|----------|--------|---------------|-------|
| List all books | `/api/books/` | GET | ❌ No | Supports filtering, searching, ordering |
| View book details | `/api/books/<id>/` | GET | ❌ No | Retrieve single book by ID |
| Create new book | `/api/books/create/` | POST | ✅ Yes | Authenticated users only |
| Update book | `/api/books/<id>/update/` | PUT / PATCH | ✅ Yes | Full (PUT) or partial (PATCH) update |
| Delete book | `/api/books/<id>/delete/` | DELETE | ✅ Yes | Authenticated users only |

**Tips:**  
- Unauthenticated users attempting write operations will get **HTTP 403 Forbidden**.  
- Use query params for advanced list filtering: `?title=...&author__name=...&publication_year=...`  
- Search with `?search=keyword` (works on `title` and `author__name`)  
- Order results with `?ordering=field` or descending with `?ordering=-field`

Create a book (authenticated):
curl -X POST "http://localhost:8000/api/books/create/" \
-H "Authorization: Token <your_token>" \
-H "Content-Type: application/json" \
-d '{"title":"New Book","author":1,"publication_year":2024}'

Update a book (authenticated):
curl -X PATCH "http://localhost:8000/api/books/1/update/" \
-H "Authorization: Token <your_token>" \
-H "Content-Type: application/json" \
-d '{"title":"Updated Book"}'

curl -X PATCH "http://localhost:8000/api/books/1/update/" \
-H "Authorization: Token <your_token>" \
-H "Content-Type: application/json" \
-d '{"title":"Updated Book"}'

Delete a book (authenticated):
curl -X DELETE "http://localhost:8000/api/books/1/delete/" \
-H "Authorization: Token <your_token>"
