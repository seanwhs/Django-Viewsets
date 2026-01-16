# 🧪 **Postman Testing Guide – DRF ViewSets Memory Project**

**Purpose:** Complete testing workflow for your **ViewSet vs ModelViewSet** comparison project. Test **JWT auth**, **public endpoints**, **slug lookups**, **all CRUD operations**. Ready-to-copy Postman setup.

***

## 🎯 **1. Postman Environment Setup**

Create **Environment Variables** (Ctrl+Alt+E):

| **Variable** | **Initial Value** | **Purpose** |
|--------------|-------------------|-------------|
| `BASE_URL` | `http://127.0.0.1:8000/api` | API root |
| `ACCESS_TOKEN` | `""` | JWT token (set after login) |
| `REFRESH_TOKEN` | `""` | Refresh token (set after login) |

***

## 🔐 **2. JWT Authentication Flow**

### **Step 1: Login → Get Tokens**
```
POST {{BASE_URL}}/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

**✅ Response (201):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**→ Copy `access` → Set `{{ACCESS_TOKEN}}`**
**→ Copy `refresh` → Set `{{REFRESH_TOKEN}}`**

***

### **Step 2: Refresh Token (when expired)**
```
POST {{BASE_URL}}/token/refresh/
Content-Type: application/json

{
  "refresh": "{{REFRESH_TOKEN}}"
}
```

**✅ Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

***

## 🌐 **3. Products API Testing (ViewSet)**

### **✅ PUBLIC: List Products (No JWT)**
```
GET {{BASE_URL}}/products/
```
**Headers:** None  
**✅ 200 OK** → Product array

***

### **🔒 PROTECTED: All Other Actions**

**Headers (ALL protected requests):**
```
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

#### **Create Product**
```
POST {{BASE_URL}}/products/
{
  "slug": "iphone-16",
  "name": "iPhone 16 Pro",
  "price": 999
}
```
**✅ 201 Created**

#### **Retrieve Product (Slug Lookup)**
```
GET {{BASE_URL}}/products/iphone-16/
```
**✅ 200 OK**

#### **Full Update**
```
PUT {{BASE_URL}}/products/iphone-16/
{
  "slug": "iphone-16",
  "name": "iPhone 16 Pro Max",
  "price": 1199
}
```

#### **Partial Update**
```
PATCH {{BASE_URL}}/products/iphone-16/
{
  "price": 1299
}
```

#### **Delete**
```
DELETE {{BASE_URL}}/products/iphone-16/
```
**✅ 204 No Content**

***

## 📱 **4. Contacts API Testing (ModelViewSet)**

**ALL endpoints require JWT** → Same headers as above.

### **List + Create**
```
GET {{BASE_URL}}/contacts/
```
```
POST {{BASE_URL}}/contacts/
{
  "fname": "John",
  "lname": "Doe"
}
```

### **CRUD by ID**
```
GET {{BASE_URL}}/contacts/1/
PUT {{BASE_URL}}/contacts/1/
PATCH {{BASE_URL}}/contacts/1/
DELETE {{BASE_URL}}/contacts/1/
```

***

## 📋 **5. Complete Endpoint Matrix**

| **Endpoint** | **Method** | **Auth** | **ViewSet** | **ModelViewSet** |
|--------------|------------|----------|-------------|------------------|
| `/products/` | **GET** | ❌ Public | ✅ List | - |
| `/products/` | **POST** | ✅ JWT | ✅ Create | - |
| `/products/<slug>/` | **GET** | ✅ JWT | ✅ Retrieve | - |
| `/products/<slug>/` | **PUT** | ✅ JWT | ✅ Update | - |
| `/products/<slug>/` | **PATCH** | ✅ JWT | ✅ Partial | - |
| `/products/<slug>/` | **DELETE** | ✅ JWT | ✅ Destroy | - |
| `/contacts/` | **GET** | ✅ JWT | - | ✅ List |
| `/contacts/` | **POST** | ✅ JWT | - | ✅ Create |
| `/contacts/<id>/` | **GET/PUT/PATCH/DELETE** | ✅ JWT | - | ✅ All |

***

## 🧩 **6. Postman Collection JSON (Import Ready)**

```json
{
  "info": { "name": "DRF ViewSets", "_postman_id": "..." },
  "variable": [
    { "key": "BASE_URL", "value": "http://127.0.0.1:8000/api" },
    { "key": "ACCESS_TOKEN", "value": "" },
    { "key": "REFRESH_TOKEN", "value": "" }
  ],
  "item": [
    {
      "name": "🔐 JWT Login",
      "request": { "method": "POST", "url": "{{BASE_URL}}/token/", ... }
    },
    {
      "name": "🌐 Products List (Public)",
      "request": { "method": "GET", "url": "{{BASE_URL}}/products/" }
    },
    {
      "name": "📱 Products Create (JWT)",
      "request": { 
        "method": "POST", 
        "url": "{{BASE_URL}}/products/",
        "header": [
          { "key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}" },
          { "key": "Content-Type", "value": "application/json" }
        ]
      }
    }
  ]
}
```

***

## ⚡ **7. Pro Tips (Save Time)**

1. **Pre-request Script** (auto-set headers):
```javascript
pm.request.headers.add({
    key: 'Authorization',
    value: 'Bearer ' + pm.environment.get('ACCESS_TOKEN')
});
```

2. **Tests Script** (auto-save tokens):
```javascript
if (pm.response.code === 200) {
  const jsonData = pm.response.json();
  pm.environment.set("ACCESS_TOKEN", jsonData.access);
  pm.environment.set("REFRESH_TOKEN", jsonData.refresh);
}
```

3. **Collection Runner** → Test all endpoints in sequence.

***

## 🚀 **8. Quickstart Workflow**

```
1. python manage.py runserver
2. Postman → Import environment
3. POST /token/ → Set tokens
4. GET /products/ → Test public
5. POST /products/ → Test JWT
6. POST /contacts/ → Test ModelViewSet
7. Open http://127.0.0.1:8000/api/docs/ → Swagger backup
```

***

## 📁 **9. Logs Check (Bonus)**

After testing, check `./logs/`:
```
api.log      → All requests logged
errors.log   → Failed auth attempts
django.log   → Framework events
```
