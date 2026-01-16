# 🎯 **DRF ViewSets Memory Palace** — **ViewSet vs ModelViewSet Deep Dive**

**Purpose:** Personal memory project comparing `ViewSet` vs `ModelViewSet` side-by-side. **Everything preserved** — JWT, logging, slug lookups, routers, permissions. Every detail documented for instant recall.

***

## 🧠 **1. ViewSet vs ModelViewSet — The Core Decision Matrix**

| **Criteria** | **ViewSet** ❌ **Manual Everything** | **ModelViewSet** ✅ **Auto Everything** |
|--------------|-------------------------------------|---------------------------------------|
| **Lines of code** | **60+** (write ALL CRUD) | **6 lines** (inherits everything) |
| **`queryset`** | Manual in each method | **One line** — shared across all |
| **`serializer_class`** | Manual instantiation | **Auto-applied** to all actions |
| **CRUD Actions** | Write `list()`, `create()`, `retrieve()`, etc. | **FREE** — all 6 actions included |
| **Lookup handling** | Manual `get_object_or_404()` | **Auto** via `lookup_field` |
| **`get_object()`** | Manual everywhere | **Built-in** — handles 404s |
| **Pagination** | Manual implementation | **Auto** via DRF settings |
| **Filtering** | Manual `filterset_class` | **Auto** with `filterset_fields` |
| **When to use** | Custom logic, non-CRUD workflows | **90%+** standard CRUD APIs |
| **Learning curve** | Understand DRF internals | Production-ready immediately |

***

## 🏗️ **2. Project Structure (Everything Preserved)**

```
config/
├── settings.py         # JWT + Swagger + Logging
├── urls.py            # /api/ + token endpoints
└── middleware.py      # DRFRequestResponseLoggingMiddleware
├── contacts/          # ModelViewSet (6 lines)
├── products/          # ViewSet (60+ lines manual CRUD)
├── logs/              # api.log, django.log, errors.log
└── db.sqlite3
```

***

## 🔐 **3. JWT Authentication (Complete Flow)**

```
POST /api/token/              → {username, password} → access + refresh
GET /api/products/            → PUBLIC ✅ (no token)
Bearer <access_token>         → ALL other endpoints
POST /api/token/refresh/      → refresh expired access token
```

**Settings preserved exactly:**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

***

## 💻 **4. Contacts App — ModelViewSet (The Winner)**

### **Model (`contacts/models.py`)**
```python
class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
```

### **Serializer (`contacts/serializers.py`)**
```python
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
```

### **Views (`contacts/views.py`) — 6 LINES TOTAL**
```python
class ContactViewSet(ModelViewSet):  # ← INHERITS EVERYTHING
    queryset = Contact.objects.all()         # 1️⃣ ONE LINE
    serializer_class = ContactSerializer     # 2️⃣ ONE LINE  
    permission_classes = [IsAuthenticated]   # 3️⃣ ALL JWT 🔒
```

### **URLs (`contacts/urls.py`)**
```python
router.register('contacts', ContactViewSet, basename='contacts')
# → AUTO: /api/contacts/, /api/contacts/1/
```

**Result:** **FULL CRUD** with **3 lines of configuration**.

***

## 🛠️ **5. Products App — ViewSet (Manual Control)**

### **Model (`products/models.py`)**
```python
class Product(models.Model):
    slug = models.SlugField(unique=True)  # ← CUSTOM LOOKUP
    name = models.CharField(max_length=100)
    price = models.IntegerField()
```

### **Views (`products/views.py`) — 60+ LINES OF MANUAL CODE**
```python
class ProductViewSet(ViewSet):  # ← NO INHERITED CRUD
    lookup_field = 'slug'  # Custom slug lookup
    
    def get_permissions(self):  # Per-action permissions
        if self.action == 'list': return [AllowAny()]      # PUBLIC ✅
        return [IsAuthenticated()]                         # JWT 🔒
    
    # ❌ MANUAL EVERYTHING:
    def list(self, request):           # GET /api/products/
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def create(self, request):         # POST /api/products/
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
    def retrieve(self, request, slug=None):  # GET /api/products/my-slug/
        product = get_object_or_404(Product, slug=slug)  # MANUAL 404
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    # ... + update(), partial_update(), destroy() — ALL MANUAL
```

**Pain points:**
- **No auto `queryset`** → repeat `Product.objects.all()`
- **No auto serializer** → manual instantiation everywhere
- **No `get_object()`** → manual `get_object_or_404()` everywhere
- **60+ lines** vs **6 lines**

***

## 📊 **6. Complete Endpoint Matrix**

| Endpoint | Method | **Contacts (ModelViewSet)** | **Products (ViewSet)** | Auth |
|----------|--------|----------------------------|----------------------|------|
| `/list/` | **GET** | ✅ `/api/contacts/` | ✅ `/api/products/` **PUBLIC** | None |
| `/list/` | **POST** | ✅ `/api/contacts/` | ✅ `/api/products/` | JWT 🔒 |
| `/detail/` | **GET** | ✅ `/api/contacts/1/` | ✅ `/api/products/my-slug/` | JWT 🔒 |
| `/detail/` | **PUT** | ✅ `/api/contacts/1/` | ✅ `/api/products/my-slug/` | JWT 🔒 |
| `/detail/` | **PATCH** | ✅ `/api/contacts/1/` | ✅ `/api/products/my-slug/` | JWT 🔒 |
| `/detail/` | **DELETE** | ✅ `/api/contacts/1/` | ✅ `/api/products/my-slug/` | JWT 🔒 |

***

## ⚙️ **7. Settings (Everything Preserved)**

```python
# JWT + Swagger
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt...'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # /api/docs/
}

# Logging (auto-creates ./logs/)
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
# api.log, django.log, errors.log
```

***

## 🚀 **8. Muscle Memory Quickstart**

```bash
pip install -r requirements.txt
python manage.py makemigrations migrate createsuperuser runserver
```

**URLs to bookmark:**
```
🌐 http://127.0.0.1:8000/api/docs/           # Swagger
📱 http://127.0.0.1:8000/api/products/       # PUBLIC list
🔐 http://127.0.0.1:8000/api/token/          # JWT login
```

***

## 🧪 **9. Curl Testing (Copy-Paste Ready)**

```bash
# 1. LOGIN → Get JWT
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# 2. PUBLIC products list
curl http://127.0.0.1:8000/api/products/

# 3. PROTECTED create product
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"slug":"test","name":"Test","price":100}'
```

***

## 🧠 **10. Memory Palace Anchors (Repeat Daily)**

```
ModelViewSet = "3 lines → FULL CRUD ✅"
ViewSet     = "60+ lines → TOTAL CONTROL ⚙️"
Router     = "register() → AUTO URLS 📡"
lookup_field = "pk → slug 🔄"
get_permissions() = "per-action auth 🎯"
```

***

## 📈 **11. When to Choose What? (Decision Tree)**

```
Need standard CRUD? → ModelViewSet ✅
Need custom actions? → ViewSet
Need non-model data? → ViewSet  
Need slug lookup? → lookup_field='slug' (both work)
Need per-action perms? → get_permissions() (both work)
```

***

## 📁 **12. Logging (Bonus Memory Trigger)**

```
./logs/ (auto-created)
├── api.log         # API requests
├── django.log      # Framework  
└── errors.log      # Exceptions
```

***

## 🎯 **Final Memory Hook**

```
Contacts = "ModelViewSet = MAGIC"
Products = "ViewSet = MANUAL = WHAT'S UNDER THE HOOD"

90% → ModelViewSet
10% → ViewSet (custom needs)

This project = ViewSets forever burned into memory 💾
```
