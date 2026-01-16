# Django REST Framework — ViewSets Learning Project

This project is designed to **demonstrate and compare different types of ViewSets** in Django REST Framework (DRF).  
It’s a practical learning project showing how both `ModelViewSet` and `ViewSet` approaches work side by side with JWT authentication and Swagger documentation.

***

## Overview

The repository includes two apps:

- **`contacts`** → built with `ModelViewSet` (concise, automatic CRUD).
- **`products`** → built with `ViewSet` (manual CRUD for learning and flexibility).

***

## Project Structure

```
├── contacts/
│   ├── models.py           # Simple Contact model
│   ├── serializers.py
│   ├── views.py            # Using ModelViewSet
│   └── urls.py             # Registered via DefaultRouter
├── products/
│   ├── models.py           # Product with slug
│   ├── serializers.py
│   ├── views.py            # Custom ViewSet with manual CRUD
│   └── urls.py             # Registered via DefaultRouter
├── config/
│   ├── settings.py         # DRF, JWT, and logging setup
│   ├── urls.py             # Combines all API routes
│   └── middleware.py       # Optional API request/response logging
├── logs/                   # Automatically created for logging
├── db.sqlite3
└── manage.py
```

***

## Authentication

The API uses **JWT (JSON Web Token)** authentication for secure endpoints via `djangorestframework-simplejwt`.

| Method | URL                     | Description               |
| ------ | ----------------------- | ------------------------- |
| POST   | `/api/token/`           | Obtain access/refresh JWT |
| POST   | `/api/token/refresh/`   | Refresh access token      |

**Authentication rules:**

- **Products**
  - `GET /api/products/` → public (no authentication)
  - All other methods require a valid JWT

- **Contacts**
  - All endpoints require JWT authentication

***

## API Endpoints

| Method | Endpoint                     | Description               | Implemented In | Auth Required? |
| ------ | ----------------------------- | ------------------------- | -------------- | -------------- |
| GET    | `/api/contacts/`              | List all contacts         | ModelViewSet   | ✅ Yes |
| POST   | `/api/contacts/`              | Create contact            | ModelViewSet   | ✅ Yes |
| GET    | `/api/contacts/<id>/`         | Retrieve contact          | ModelViewSet   | ✅ Yes |
| PUT    | `/api/contacts/<id>/`         | Full update               | ModelViewSet   | ✅ Yes |
| PATCH  | `/api/contacts/<id>/`         | Partial update            | ModelViewSet   | ✅ Yes |
| DELETE | `/api/contacts/<id>/`         | Delete contact            | ModelViewSet   | ✅ Yes |
| GET    | `/api/products/`              | List all products         | Custom ViewSet | ❌ No |
| POST   | `/api/products/`              | Create product            | Custom ViewSet | ✅ Yes |
| GET    | `/api/products/<slug>/`       | Retrieve by slug          | Custom ViewSet | ✅ Yes |
| PUT    | `/api/products/<slug>/`       | Full update               | Custom ViewSet | ✅ Yes |
| PATCH  | `/api/products/<slug>/`       | Partial update            | Custom ViewSet | ✅ Yes |
| DELETE | `/api/products/<slug>/`       | Delete product            | Custom ViewSet | ✅ Yes |

***

## Key Learning Comparison

| Feature                              | `contacts` (ModelViewSet)         | `products` (ViewSet)                         |
| ------------------------------------ | --------------------------------- | -------------------------------------------- |
| Base class                           | `ModelViewSet`                    | `ViewSet`                                    |
| Boilerplate                          | Minimal (automatic CRUD)          | High (manual CRUD)                           |
| Queryset & serializer auto-handling  | ✅ Yes                            | ❌ No                                        |
| Lookup customization                 | Simple via `lookup_field`         | Manual (defined in methods)                  |
| JWT enforcement                      | Required for all endpoints        | Optional (public list)                       |
| When to use                          | Standard CRUD APIs                | Custom workflows or business logic           |
| Router compatible                    | ✅ Yes                            | ✅ Yes                                       |
| Learning takeaway                    | Use by default                    | Learn how DRF views work internally          |

***

## Quick Start

```bash
# 1. Clone repo & setup virtual environment
git clone <your-repo-url>
cd <repo-folder>
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations & create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 4. Run the development server
python manage.py runserver
```

Visit the API UI:

- 🌐 http://127.0.0.1:8000/api/docs/ → Swagger UI
- 🌐 http://127.0.0.1:8000/api/redoc/ → ReDoc
- 🧱 http://127.0.0.1:8000/api/schema/ → OpenAPI schema

***

## Endpoint Access Flow

### Products

```text
/api/products/
  ├── GET (Public — no JWT)
  └── [Authenticated actions: POST, PUT, PATCH, DELETE]
       require Bearer <access_token>
```

### Contacts

```text
/api/contacts/
  ├── GET, POST
  └── /api/contacts/<id>/ → GET, PUT, PATCH, DELETE
       (All require JWT authentication)
```

***

## Swagger & Logging

- **DRF Spectacular** powers `/api/docs/` and `/api/redoc/`.
- **Custom logging** saves logs into `./logs/` automatically:
  - `api.log` → general API operations  
  - `django.log` → framework-level logs  
  - `errors.log` → request exceptions

***

## Suggested Exercises

1. Add custom actions with `@action(detail=True)` in `ProductViewSet`.
2. Implement DRF pagination and filtering for `ProductViewSet`.
3. Try converting `ProductViewSet` into a `ModelViewSet` and compare.
4. Add `IsAdminUser` or `IsOwnerOrReadOnly` permissions.
5. Extend `Contact` with phone/email fields and validation.
6. Deploy to production with proper secret keys and logging settings.

***

Happy coding and exploring DRF ViewSets! 🚀