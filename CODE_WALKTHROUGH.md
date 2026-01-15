# Code Walkthrough – DRF ViewSets Project

This guide walks you through the **contacts** and **products** apps, explaining **ModelViewSet vs custom ViewSet**, CRUD logic, and **JWT integration**.

---

## 1. Root URL Configuration

**File:** `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('contacts.urls')),
]
```

* All API endpoints are under `/api/`.
* `products` and `contacts` are included via **routers**.
* Admin panel is at `/admin/`.

---

## 2. Contacts App

### 2.1 Model

**File:** `contacts/models.py`

```python
from django.db import models

class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)

    def __str__(self):
        return self.lname
```

* Simple model with `fname` and `lname`.
* `__str__` helps Django admin display readable names.

---

### 2.2 Serializer

**File:** `contacts/serializers.py`

```python
from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
```

* `ModelSerializer` automatically handles CRUD fields.

---

### 2.3 Views

**File:** `contacts/views.py`

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]  # JWT required for all actions
```

* `ModelViewSet` provides all CRUD endpoints automatically.
* Permissions: JWT enforced via `IsAuthenticated`.

---

### 2.4 URLs

**File:** `contacts/urls.py`

```python
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter()
router.register('contacts', ContactViewSet, basename='contacts')

urlpatterns = router.urls
```

* `DefaultRouter` generates URLs for `list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`.

---

## 3. Products App

### 3.1 Model

**File:** `products/models.py`

```python
from django.db import models

class Product(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
```

* Products are identified by **slug**.
* `price` stored as integer for simplicity.

---

### 3.2 Serializer

**File:** `products/serializers.py`

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

* Standard `ModelSerializer` for JSON ↔ model conversion.

---

### 3.3 Views

**File:** `products/views.py`

```python
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ViewSet):
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug):
        product = get_object_or_404(Product.objects.all(), slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, slug):
        product = get_object_or_404(Product.objects.all(), slug=slug)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, slug):
        product = get_object_or_404(Product.objects.all(), slug=slug)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, slug):
        product = get_object_or_404(Product.objects.all(), slug=slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Highlights:**

* Manual CRUD logic gives **fine-grained control**.
* `get_permissions` allows **public listing** and **JWT-protected actions**.
* Slug-based lookup implemented via `lookup_field` + `get_object_or_404`.

---

### 3.4 URLs

**File:** `products/urls.py`

```python
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = router.urls
```

* Router automatically generates `/api/products/` and `/api/products/<slug>/`.

---

## 4. JWT Authentication

**Settings (`settings.py`):**

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

* JWT globally enabled.
* Permissions overridden per-view (`get_permissions`).
* Tokens:

  * `/api/token/` → get access & refresh tokens
  * `/api/token/refresh/` → refresh access token

---

## 5. API Access Overview

### Products

| Endpoint                | Methods                       | Access   |
| ----------------------- | ----------------------------- | -------- |
| `/api/products/`        | GET (list)                    | Public   |
| `/api/products/<slug>/` | GET, POST, PUT, PATCH, DELETE | JWT Only |

### Contacts

| Endpoint              | Methods                 | Access   |
| --------------------- | ----------------------- | -------- |
| `/api/contacts/`      | GET, POST               | JWT Only |
| `/api/contacts/<id>/` | GET, PUT, PATCH, DELETE | JWT Only |

---

## 6. Postman Testing Workflow

1. `POST /api/token/` → obtain access & refresh JWT tokens.
2. `GET /api/products/` → public, no token needed.
3. Other product endpoints → include token in `Authorization: Bearer <access_token>`.
4. Contacts endpoints → all require JWT.
5. `POST /api/token/refresh/` → refresh token when access expires.

---

### ✅ Key Learning Points

* `ModelViewSet` → quick CRUD, automatic routing.
* `ViewSet` → full control, custom logic, per-action permissions.
* JWT authentication can be **global** or **per-action**.
* Slug-based lookups via `lookup_field` + `get_object_or_404`.
* Router handles URLs, reducing boilerplate.

---

### 7. Visual Flow Diagram

```text
Products:
┌─────────────────────┐
│ /api/products/      │ GET → Public
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ /api/products/<slug>│ GET, POST, PUT, PATCH, DELETE → JWT
└─────────────────────┘

Contacts:
┌─────────────────────┐
│ /api/contacts/      │ GET, POST → JWT
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ /api/contacts/<id>  │ GET, PUT, PATCH, DELETE → JWT
└─────────────────────┘
```

---

This **cleaned-up walkthrough** is ready to include in your README or a separate markdown file. It covers:

* Structure
* Models & serializers
* ViewSets logic
* JWT authentication
* URL routing
* Postman testing
* Public vs JWT-protected endpoints

