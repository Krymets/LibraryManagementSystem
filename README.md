# 📚 Library Management System

A Django REST Framework-based application for managing a library. Users can register, search for books, and borrow them. Admins can manage users and inventory.

---

## 🚀 Features

- ✅ JWT Authentication (login/register)
- 🔍 Book search with filtering and pagination
- 📚 Borrow and return books (Loan system)
- 🧑‍💼 Role-based access: Anonymous, Registered Users, Admins
- 📄 Swagger & ReDoc API documentation
- 🐳 Docker support
- 🧪 Unit & integration tests (Pytest)
- 🛡️ Protection from CSRF, XSS, SQL Injection

---

## 🏗 Tech Stack

- **Backend**: Django 5, DRF, PostgreSQL
- **Auth**: JWT (`djangorestframework-simplejwt`)
- **API Docs**: `drf-yasg`
- **Filtering**: `django-filter`
- **Tests**: `pytest`, `pytest-django`
- **Containerization**: Docker, Docker Compose
- **Deployment Ready**: Heroku or any platform

---

## ⚙️ Setup Instructions

### 📦 Installation (Local)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system

2. Create virtual environment:
   ```bash
    python3 -m venv .venv
    source .venv/bin/activate

3. Install dependencies:
   ```bash
    pip install -r requirements.txt

4. Apply migrations:
   ```bash
    python manage.py migrate
   
5. Run server:
   ```bash
    python manage.py runserver

### 🐳 Docker
1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build

## 🔐 Authentication
### Register
1. POST /api/auth/register/
   ```json
   {
     "username": "user",
     "email": "user@example.com",
     "password": "VeryStrongPassword123!"
   }

### Login
1. POST /api/auth/login/
   ```json
   {
     "username": "user",
     "password": "VeryStrongPassword123!"
   }

## 📘 API Endpoints
📘 API Endpoints
- `GET /api/books/` – List books  
  - Supports pagination: `?page=2`  
  - Supports filtering: `?author=Rowling&availability=True`  
  - Supports search: `?search=harry`  
  - Supports ordering: `?ordering=title`  

- `POST /api/loans/` – Borrow a book
- `POST /api/return/<book_id>/` – Return a book
- `GET /swagger/` – Swagger UI
- `GET /redoc/` – ReDoc documentation

## 🧪 Tests
### Includes:
1. ✅ Unit tests for models and serializers
2. ✅ Integration tests for registration, login, and borrowing
   ```bash
   pytest

## 📑 License
MIT License. Feel free to use and adapt.

## ✍️ Author
Created by [@Krymets](https://github.com/Krymets)
