# Django REST Framework - ViewSets Learning Project

This is a simple project created to help understand and compare different ways of implementing **ViewSets** in Django REST Framework (DRF).

The repository contains **two apps** demonstrating different approaches:

* `contacts` → using **ModelViewSet** (most common & recommended way)
* `products` → using **ViewSet** (manual implementation, more control, more code, JWT-secured)

---

## Project Structure

```
├── contacts/
│   ├── models.py          # Simple Contact model
│   ├── serializers.py
│   ├── views.py           → Using ModelViewSet
│   └── urls.py            → Using DefaultRouter
├── products/
│   ├── models.py          # Product model with slug
│   ├── serializers.py
│   ├── views.py           → Custom ViewSet (manual CRUD)
│   └── urls.py            → Using DefaultRouter
├── api/                   # Included in root urls.py
└── README.md
```

---

## Authentication

This project uses **JWT authentication** for protected actions.

* **Products**:

  * `list` → public, no authentication required
  * All other actions (`retrieve`, `create`, `update`, `partial_update`, `delete`) → JWT required

* **Contacts**:

  * All endpoints require JWT authentication

JWT endpoints:

| Method | URL                   | Description                 |
| ------ | --------------------- | --------------------------- |
| POST   | `/api/token/`         | Get access & refresh tokens |
| POST   | `/api/token/refresh/` | Refresh access token        |

---

## Available API Endpoints

| Method | URL                     | Description              | Implemented in | Auth Required? |
| ------ | ----------------------- | ------------------------ | -------------- | -------------- |
| GET    | `/api/contacts/`        | List all contacts        | ModelViewSet   | ✅ Yes          |
| POST   | `/api/contacts/`        | Create new contact       | ModelViewSet   | ✅ Yes          |
| GET    | `/api/contacts/<id>/`   | Get single contact       | ModelViewSet   | ✅ Yes          |
| PUT    | `/api/contacts/<id>/`   | Update contact (full)    | ModelViewSet   | ✅ Yes          |
| PATCH  | `/api/contacts/<id>/`   | Update contact (partial) | ModelViewSet   | ✅ Yes          |
| DELETE | `/api/contacts/<id>/`   | Delete contact           | ModelViewSet   | ✅ Yes          |
| GET    | `/api/products/`        | List all products        | Custom ViewSet | ❌ No           |
| POST   | `/api/products/`        | Create new product       | Custom ViewSet | ✅ Yes          |
| GET    | `/api/products/<slug>/` | Get product by slug      | Custom ViewSet | ✅ Yes          |
| PUT    | `/api/products/<slug>/` | Update product (full)    | Custom ViewSet | ✅ Yes          |
| PATCH  | `/api/products/<slug>/` | Update product (partial) | Custom ViewSet | ✅ Yes          |
| DELETE | `/api/products/<slug>/` | Delete product           | Custom ViewSet | ✅ Yes          |

---

## Key Learning Points

| Topic                             | `contacts` app               | `products` app                           |
| --------------------------------- | ---------------------------- | ---------------------------------------- |
| Base class used                   | `ModelViewSet`               | `ViewSet`                                |
| Amount of code needed             | Very little                  | A lot (manual implementation)            |
| Queryset & serializer auto-config | Yes                          | No - you write everything                |
| Lookup field customization        | Easy (`lookup_field`)        | Possible but manual                      |
| Permissions / authentication      | JWT enforced for all actions | Public list, JWT for others              |
| When would you use this?          | 90%+ of normal CRUD APIs     | Very custom logic, special actions       |
| Router support                    | Yes                          | Yes                                      |
| Recommended for learning?         | ★ First choice               | ★ Understand what's happening underneath |

---

## Quick Start

```bash
# 1. Clone & setup virtual environment
git clone <your-repo-url>
cd <repo-folder>
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install django djangorestframework djangorestframework-simplejwt

# 3. Apply migrations & create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 4. Run the server
python manage.py runserver
```

Visit the API:

* [Contacts List](http://127.0.0.1:8000/api/contacts/)
* [Products List](http://127.0.0.1:8000/api/products/)
* [Product Detail](http://127.0.0.1:8000/api/products/your-product-slug/)

JWT endpoints:

* [Get Token](http://127.0.0.1:8000/api/token/)
* [Refresh Token](http://127.0.0.1:8000/api/token/refresh/)

---

## Endpoint Access Diagrams

### Products

```text
                  ┌─────────────────────────┐
                  │   /api/products/        │
                  │   (GET - list)          │
                  │   Public (No JWT)       │
                  └───────────┬────────────┘
                              │
                  ┌───────────▼────────────┐
                  │  /api/products/<slug>/ │
                  │  (GET, POST, PUT,      │
                  │   PATCH, DELETE)       │
                  │  JWT required           │
                  └────────────────────────┘
```

Or Markdown table:

| Endpoint                | Method          | Access   |
| ----------------------- | --------------- | -------- |
| `/api/products/`        | GET (list)      | Public   |
| `/api/products/<slug>/` | GET (retrieve)  | JWT Only |
| `/api/products/<slug>/` | POST (create)   | JWT Only |
| `/api/products/<slug>/` | PUT (update)    | JWT Only |
| `/api/products/<slug>/` | PATCH (partial) | JWT Only |
| `/api/products/<slug>/` | DELETE          | JWT Only |

### Contacts

```text
                  ┌─────────────────────────┐
                  │    /api/contacts/       │
                  │  (GET, POST)            │
                  │  JWT required           │
                  └───────────┬────────────┘
                              │
                  ┌───────────▼────────────┐
                  │  /api/contacts/<id>/   │
                  │  (GET, PUT, PATCH,     │
                  │   DELETE)              │
                  │  JWT required           │
                  └────────────────────────┘
```

Or Markdown table:

| Endpoint              | Method          | Access   |
| --------------------- | --------------- | -------- |
| `/api/contacts/`      | GET (list)      | JWT Only |
| `/api/contacts/`      | POST (create)   | JWT Only |
| `/api/contacts/<id>/` | GET (retrieve)  | JWT Only |
| `/api/contacts/<id>/` | PUT (update)    | JWT Only |
| `/api/contacts/<id>/` | PATCH (partial) | JWT Only |
| `/api/contacts/<id>/` | DELETE          | JWT Only |

✅ Notes:

* **Products**: `list` is public, all others require JWT
* **Contacts**: All endpoints require JWT

---

## Next Steps / Exercises Ideas

1. Add more fine-grained `permission_classes`
2. Add custom actions with `@action(detail=True, methods=['post'])` in products
3. Try `ReadOnlyModelViewSet` for contacts
4. Implement filtering/search/pagination on products
5. Refactor products to use `ModelViewSet` → see how much shorter it becomes
6. Add more authentication methods (Session, Token, OAuth)

Happy learning! 🚀


