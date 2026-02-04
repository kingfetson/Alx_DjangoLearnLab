# Advanced API Project (Django & Django REST Framework)

This project is part of the **ALX Django Learn Lab**. It demonstrates how to set up a Django project with **Django REST Framework (DRF)**, define relational models, create custom serializers with validation, and test the implementation.

> **Note on naming:**
> The project directory may be named `advanced-api-project`, but the Django project itself is named `advanced_api_project` because Django (and Python) do not allow hyphens in module names.

---

## 📌 Project Overview

The project implements:

* A Django project configured with Django REST Framework
* Two related models: **Author** and **Book** (one-to-many relationship)
* Custom serializers with nested serialization
* Validation to prevent invalid data entry
* Manual testing using Django shell or Django admin

---

## 🛠 Technologies Used

* Python 3
* Django
* Django REST Framework
* SQLite (default Django database)

---

## 📁 Project Structure

```
advanced-api-project/
│── manage.py
│── advanced_api_project/
│   │── __init__.py
│   │── settings.py
│   │── urls.py
│   │── asgi.py
│   │── wsgi.py
│── api/
│   │── migrations/
│   │── __init__.py
│   │── admin.py
│   │── apps.py
│   │── models.py
│   │── serializers.py
│   │── views.py
│   │── tests.py
│── db.sqlite3
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Alx_DjangoLearnLab.git
cd advanced-api-project
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework
```

(Optional)

```bash
pip freeze > requirements.txt
```

---

## ⚙️ Project Configuration

### Installed Apps

In `advanced_api_project/settings.py`, the following apps are enabled:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'api',
]
```

### Database

The project uses **SQLite**, Django’s default database configuration.

---

## 🧩 Models

### Author Model

* `name` – stores the author’s name

### Book Model

* `title` – book title
* `publication_year` – year the book was published
* `author` – foreign key linking a book to an author

**Relationship:**

* One **Author** can have many **Books**
* Implemented using `ForeignKey` with `related_name='books'`

---

## 🔄 Serializers

### BookSerializer

* Serializes all fields of the `Book` model
* Includes custom validation to ensure `publication_year` is not in the future

### AuthorSerializer

* Serializes the `Author` model
* Includes a nested list of related books using `BookSerializer`

---

## 🧪 Running Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Testing the Project

### Option 1: Django Shell

```bash
python manage.py shell
```

```python
from api.models import Author, Book
from api.serializers import AuthorSerializer

author = Author.objects.create(name="Ngũgĩ wa Thiong’o")
Book.objects.create(title="Petals of Blood", publication_year=1977, author=author)

serializer = AuthorSerializer(author)
print(serializer.data)
```

### Option 2: Django Admin

1. Register models in `api/admin.py`
2. Create a superuser:

```bash
python manage.py createsuperuser
```

3. Run the server and access `/admin`

```bash
python manage.py runserver
```

---

## ✅ Verification Checks

```bash
python manage.py check
python manage.py runserver
```

Expected output:

```
System check identified no issues (0 silenced).
```

---

## 📦 Repository Information

* **Repository:** Alx_DjangoLearnLab
* **Directory:** advanced-api-project

---

## ✍️ Author

**Festus** – ALX Software Engineering Program

---

## 📄 License

This project is for educational purposes under the ALX program.
