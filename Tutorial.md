# 🎓 **Tutorial: DRF ViewSets + JWT + Production Logging**

***

## **📋 Table of Contents**
1. [Environment Setup](#step-1)
2. [Django Project Creation](#step-2)
3. [Settings Deep Dive](#step-3)
4. [Logging Middleware](#step-4)
5. [Main URLs](#step-5)
6. [Contacts App - ModelViewSet](#step-6)
7. [Products App - ViewSet](#step-7)
8. [Migrations & Testing](#step-8)
9. [Logging Analysis](#step-9)

***

## **Step 1: Environment Setup - Every Command**

```bash
# 🆕 Create project directory
mkdir drf-viewsets-memory
cd drf-viewsets-memory

# 🆕 Virtual environment (dependency isolation)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 🆕 Install EXACT dependencies from your requirements
pip install Django==6.0.1 djangorestframework==3.16.1 \
    djangorestframework_simplejwt==5.5.1 drf-spectacular==0.29.0 \
    drf-spectacular-sidecar==2026.1.1
```

**Create `requirements.txt` (copy exactly):**
```txt
asgiref==3.11.0
attrs==25.4.0
Django==6.0.1
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
drf-spectacular==0.29.0
drf-spectacular-sidecar==2026.1.1
inflection==0.5.1
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
PyJWT==2.10.1
PyYAML==6.0.3
referencing==0.37.0
rpds-py==0.30.0
sqlparse==0.5.5
typing_extensions==4.15.0
tzdata==2025.3
uritemplate==4.2.0
```

***

## **Step 2: Django Project Creation - EXACT Structure**

```bash
# 🆕 Main project (config = settings/urls home)
django-admin startproject config .

# 🆕 NO "mkdir config/middleware" - middleware goes in config/ directly
touch config/middleware.py

# 🆕 Two apps for ViewSet comparison
python manage.py startapp products
python manage.py startapp contacts
```

**✅ Current structure:**
```
drf-viewsets-memory/
├── config/
│   ├── __init__.py
│   ├── settings.py          # ← Replace this
│   ├── urls.py             # ← Replace this  
│   ├── wsgi.py
│   └── middleware.py       # ← Create this (NO folder)
├── products/               # ← ViewSet (manual CRUD)
├── contacts/               # ← ModelViewSet (6 lines)
├── manage.py
└── requirements.txt
```

***

## **Step 3: Settings.py - COMPLETE Production Config**

**🔥 Replace `config/settings.py` ENTIRELY:**

```python
import os
from pathlib import Path
from datetime import timedelta
import logging
from django.utils.log import DEFAULT_LOGGING

# 🆕 Root directory (manage.py location)
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔥 LOGS FOLDER - AUTO-CREATED ON STARTUP
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)  # Creates ./logs/ automatically

# 🚨 DEV SECURITY WARNING
SECRET_KEY = 'django-insecure-dev-key-change-in-production-2026x9zqwk'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Django core (must be first)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🔥 DRF + JWT + SWAGGER
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',

    # 🆕 YOUR APPS (always last)
    'products',    # ViewSet demo
    'contacts',    # ModelViewSet demo
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'config.middleware.DRFRequestResponseLoggingMiddleware',  # 🆕 YOUR LOGGING
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# 🔥 DRF + JWT CONFIG (production ready)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # Override per-view
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Swagger magic
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),    # Short-lived
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),       # Long-lived  
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Products & Contacts API - ViewSets Demo",
    "DESCRIPTION": "ModelViewSet vs ViewSet + JWT + Logging",
    "VERSION": "1.0.0",
}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation (security)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔥🔥🔥 LOGGING SYSTEM - 3 FILES EXPLAINED
LOGGING = DEFAULT_LOGGING.copy()
LOGGING['version'] = 1
LOGGING['disable_existing_loggers'] = False

# 1️⃣ FORMATTER (compact API logs)
LOGGING['formatters']['api'] = {
    'format': '[{levelname}] {asctime} {name} {message}',
    'style': '{',
}

# 2️⃣ HANDLERS (3 different files)
LOGGING['handlers']['api_file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': str(LOG_DIR / 'api.log'),     # API requests
    'formatter': 'api',
}

LOGGING['handlers']['django_file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler', 
    'filename': str(LOG_DIR / 'django.log'),  # Framework events
    'formatter': 'api',
}

LOGGING['handlers']['error_file'] = {
    'level': 'ERROR',
    'class': 'logging.FileHandler',
    'filename': str(LOG_DIR / 'errors.log'),  # Exceptions only
    'formatter': 'api',
}

# 3️⃣ LOGGERS (different scopes)
LOGGING['loggers']['api.requests'] = {      # 🆕 YOUR MIDDLEWARE USES THIS
    'handlers': ['api_file'],
    'level': 'INFO',
    'propagate': False,
}

LOGGING['loggers']['django'] = {
    'handlers': ['console', 'django_file'],
    'level': 'INFO',
    'propagate': False,
}

LOGGING['loggers']['django.request'] = {
    'handlers': ['error_file'],
    'level': 'ERROR',
    'propagate': False,
}
```

***

## **Step 4: Logging Middleware - `config/middleware.py`**

```python
"""
🔥 DRFRequestResponseLoggingMiddleware
Logs EVERY /api/ request + response automatically!

SAMPLE OUTPUT in ./logs/api.log:
[INFO] REQUEST: GET /api/products/ - User: AnonymousUser
[INFO] RESPONSE: GET /api/products/ - Status: 200
"""

import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('api.requests')  # 🆕 Matches settings LOGGING

class DRFRequestResponseLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/'):
            logger.info(f"REQUEST: {request.method} {request.path} - User: {request.user}")
        return None

    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            logger.info(f"RESPONSE: {request.method} {request.path} - Status: {response.status_code}")
        return response
```

***

## **Step 5: Main URLs - `config/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularSwaggerView, 
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🔥 AUTO-GENERATED SWAGGER FROM YOUR VIEWSETS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # 🆕 ROUTERS AUTO-GENERATE REST URLs
    path('api/', include('products.urls')),
    path('api/', include('contacts.urls')),
    
    # 🔥 JWT ENDPOINTS (no code needed!)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

***

## **Step 6: Contacts App - ModelViewSet (6 Lines Magic)**

**`contacts/models.py`:**
```python
from django.db import models

class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)

    def __str__(self):
        return self.lname
```

**`contacts/serializers.py`:**
```python
from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
```

**`contacts/views.py` - 6 LINES TOTAL!**
```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]  # 🔒 ALL JWT
```

**`contacts/urls.py`:**
```python
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter()
router.register('contacts', ContactViewSet, basename='contacts')
urlpatterns = router.urls
```

**`contacts/admin.py`:**
```python
from django.contrib import admin
from .models import Contact
admin.site.register(Contact)
```

***

## **Step 7: Products App - ViewSet (Manual CRUD)**

**`products/models.py`:**
```python
from django.db import models

class Product(models.Model):
    slug = models.SlugField(unique=True)  # 🆕 SLUG LOOKUPS
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
```

**`products/serializers.py`:**
```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

**`products/views.py` - FULL MANUAL IMPLEMENTATION:**
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
            return [AllowAny()]  # ✅ Public list
        return [IsAuthenticated()]  # 🔒 JWT everything else

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**`products/urls.py`:**
```python
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
urlpatterns = router.urls
```

**`products/admin.py`:**
```python
from django.contrib import admin
from .models import Product
admin.site.register(Product)
```

***

## **Step 8: Migrations & Launch**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# admin / admin123
python manage.py runserver
```

**✅ `./logs/` folder created automatically with 3 files!**

***

## **Step 9: Testing Matrix**

| **URL** | **Method** | **Auth** | **App** | **Status** |
|---------|------------|----------|---------|------------|
| `/api/products/` | GET | None ✅ | Products | 200 Public |
| `/api/products/` | POST | JWT 🔒 | Products | 201 |
| `/api/products/my-slug/` | GET/PUT/PATCH/DELETE | JWT 🔒 | Products | 200/204 |
| `/api/contacts/` | GET/POST | JWT 🔒 | Contacts | 200 |
| `/api/contacts/1/` | GET/PUT/PATCH/DELETE | JWT 🔒 | Contacts | 200/204 |

**Test commands:**
```bash
# 1. JWT Login
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'

# 2. Public products
curl http://127.0.0.1:8000/api/products/

# 3. Swagger UI
http://127.0.0.1:8000/api/docs/
```

***

## **Step 10: Logging Breakdown**

**After any API call → `./logs/` contains:**

```
api.log:      [INFO] REQUEST: GET /api/products/ - User: AnonymousUser
              [INFO] RESPONSE: GET /api/products/ - Status: 200

django.log:   Framework startup messages

errors.log:   404s, 500s, auth failures
```

***