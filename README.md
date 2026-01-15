# Django REST Framework - ViewSets Learning Project

This is a simple project created to help understand and compare different ways of implementing **ViewSets** in Django REST Framework (DRF).

The repository contains **two apps** demonstrating different approaches:

- `contacts` → using **ModelViewSet** (most common & recommended way)
- `products` → using **ViewSet** (manual implementation - more control, more code)

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
│   ├── views.py           → Manual ViewSet (no ModelViewSet!)
│   └── urls.py            → Using DefaultRouter
├── api/                   # Included in root urls.py
└── README.md
```

## Available API Endpoints

| Method   | URL                        | Description                        | Implemented in      |
|----------|----------------------------|------------------------------------|---------------------|
| GET      | `/api/contacts/`           | List all contacts                  | ModelViewSet        |
| POST     | `/api/contacts/`           | Create new contact                 | ModelViewSet        |
| GET      | `/api/contacts/<id>/`      | Get single contact                 | ModelViewSet        |
| PUT      | `/api/contacts/<id>/`      | Update contact (full)              | ModelViewSet        |
| PATCH    | `/api/contacts/<id>/`      | Update contact (partial)           | ModelViewSet        |
| DELETE   | `/api/contacts/<id>/`      | Delete contact                     | ModelViewSet        |
|----------|----------------------------|------------------------------------|---------------------|
| GET      | `/api/products/`           | List all products                  | Custom ViewSet      |
| POST     | `/api/products/`           | Create new product                 | Custom ViewSet      |
| GET      | `/api/products/<slug>/`    | Get product by slug                | Custom ViewSet      |
| PUT      | `/api/products/<slug>/`    | Update product (full)              | Custom ViewSet      |
| PATCH    | `/api/products/<slug>/`    | Update product (partial)           | Custom ViewSet      |
| DELETE   | `/api/products/<slug>/`    | Delete product                     | Custom ViewSet      |

## Key Learning Points

| Topic                              | `contacts` app               | `products` app                     |
|------------------------------------|------------------------------|-------------------------------------|
| Base class used                    | `ModelViewSet`               | `ViewSet`                           |
| Amount of code needed              | Very little                  | A lot (manual implementation)       |
| Queryset & serializer auto-config  | Yes                          | No - you write everything           |
| Lookup field customization         | Easy (`lookup_field`)        | Possible but manual                 |
| When would you use this?           | 90%+ of normal CRUD APIs     | Very custom logic, special actions  |
| Router support                     | Yes                          | Yes                                 |
| Recommended for learning?          | ★ First choice               | ★ Understand what's happening underneath |

## Quick Start

```bash
# 1. Clone & setup virtual environment
git clone <your-repo-url>
cd <repo-folder>
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install django djangorestframework

# 3. Apply migrations & create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 4. Run the server
python manage.py runserver
```

Then visit:

- http://127.0.0.1:8000/api/contacts/
- http://127.0.0.1:8000/api/products/
- http://127.0.0.1:8000/api/products/your-product-slug/

Also available:  
http://127.0.0.1:8000/api/ (root API view - if you add `rest_framework.urls`)

## Next Steps / Exercises Ideas

1. Add `permission_classes` to both viewsets
2. Add custom action `@action(detail=True, methods=['post'])` in products
3. Try to use `ReadOnlyModelViewSet` for contacts
4. Implement filtering/search/pagination on products
5. Change products to use `ModelViewSet` → see how much shorter it becomes!
6. Add authentication (Token / JWT)

Happy learning! 🚀