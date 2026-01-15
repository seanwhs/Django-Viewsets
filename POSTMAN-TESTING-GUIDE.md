# Postman Testing Guide – DRF ViewSets Project

This guide explains how to test the **Contacts** and **Products** APIs using **Postman**, including **JWT authentication** and environment variables.

> **All JWT-protected requests must include headers:**

```http
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

---

## 1. Setup Postman

1. Download and install [Postman](https://www.postman.com/downloads/).
2. Open Postman and create a **new collection** called `DRF ViewSets Project`.
3. Create a **Postman Environment** with variables:

| Key             | Value                       |
| --------------- | --------------------------- |
| `BASE_URL`      | `http://127.0.0.1:8000/api` |
| `ACCESS_TOKEN`  | *(set after login)*         |
| `REFRESH_TOKEN` | *(set after login)*         |

> Use `{{BASE_URL}}` in URLs and `{{ACCESS_TOKEN}}` in headers.

---

## 2. Test Public Products Endpoint

**List products (no JWT required)**

* **Method:** GET
* **URL:** `{{BASE_URL}}/products/`
* **Headers:** None
* **Body:** None

✅ Response: JSON array of products.

---

## 3. Obtain JWT Tokens

**Endpoint:** `/token/` (POST)

* **Method:** POST
* **URL:** `{{BASE_URL}}/token/`
* **Headers:**

```http
Content-Type: application/json
```

* **Body (raw JSON):**

```json
{
  "username": "your_superuser_username",
  "password": "your_superuser_password"
}
```

**Response:**

```json
{
  "access": "<access-token>",
  "refresh": "<refresh-token>"
}
```

* Copy `access` → set as `{{ACCESS_TOKEN}}`
* Copy `refresh` → set as `{{REFRESH_TOKEN}}`

---

## 4. Use JWT in Postman

For all **JWT-protected requests**, add headers:

```http
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json
```

💡 Tip: Save headers in your collection to avoid repetition.

---

## 5. Products API – Protected Endpoints

All endpoints except `GET /products/` require JWT.

### 5.1 Create Product

* **Method:** POST
* **URL:** `{{BASE_URL}}/products/`
* **Headers:** Authorization + Content-Type
* **Body (JSON):**

```json
{
  "slug": "test-product",
  "name": "Test Product",
  "price": 100
}
```

✅ Response: **201 Created**

---

### 5.2 Retrieve Product

* **Method:** GET
* **URL:** `{{BASE_URL}}/products/test-product/`
* **Headers:** Authorization + Content-Type

✅ Response: Product JSON

---

### 5.3 Update Product (Full)

* **Method:** PUT
* **URL:** `{{BASE_URL}}/products/test-product/`
* **Headers:** Authorization + Content-Type
* **Body (JSON):**

```json
{
  "slug": "test-product",
  "name": "Updated Product",
  "price": 120
}
```

✅ Response: Updated product JSON

---

### 5.4 Partial Update Product

* **Method:** PATCH
* **URL:** `{{BASE_URL}}/products/test-product/`
* **Headers:** Authorization + Content-Type
* **Body (JSON):**

```json
{
  "price": 150
}
```

✅ Response: Partially updated product

---

### 5.5 Delete Product

* **Method:** DELETE
* **URL:** `{{BASE_URL}}/products/test-product/`
* **Headers:** Authorization + Content-Type

✅ Response: **204 No Content**

---

## 6. Contacts API – All JWT-Protected

All endpoints require JWT.

### 6.1 List Contacts

* **Method:** GET
* **URL:** `{{BASE_URL}}/contacts/`
* **Headers:** Authorization + Content-Type

✅ Response: JSON array of contacts

---

### 6.2 Create Contact

* **Method:** POST
* **URL:** `{{BASE_URL}}/contacts/`
* **Headers:** Authorization + Content-Type
* **Body (JSON):**

```json
{
  "fname": "John",
  "lname": "Doe"
}
```

✅ Response: Created contact JSON

---

### 6.3 Retrieve / Update / Delete Contact

* **URL:** `{{BASE_URL}}/contacts/<id>/`
* **Methods:** GET, PUT, PATCH, DELETE
* **Headers:** Authorization + Content-Type

---

## 7. Refresh JWT Token

**Endpoint:** `/token/refresh/` (POST)

* **Method:** POST
* **URL:** `{{BASE_URL}}/token/refresh/`
* **Headers:**

```http
Content-Type: application/json
```

* **Body (JSON):**

```json
{
  "refresh": "{{REFRESH_TOKEN}}"
}
```

✅ Response: New access token → update `{{ACCESS_TOKEN}}`

---

## 8. Quick Tips

* Use **environment variables** for `BASE_URL`, `ACCESS_TOKEN`, `REFRESH_TOKEN`.
* Save requests in the collection for fast testing.
* Access rules summary:

| Endpoint            | Methods                       | Auth Required |
| ------------------- | ----------------------------- | ------------- |
| `/products/`        | GET (list)                    | ❌ Public      |
| `/products/<slug>/` | GET, POST, PUT, PATCH, DELETE | ✅ JWT Only    |
| `/contacts/`        | GET, POST                     | ✅ JWT Only    |
| `/contacts/<id>/`   | GET, PUT, PATCH, DELETE       | ✅ JWT Only    |

* Refresh your access token before expiry to continue testing protected endpoints.

---

✅ **Workflow Summary**

1. Obtain JWT tokens (`/token/`)
2. Test public endpoints (`GET /products/`)
3. Test protected endpoints with Bearer token
4. Refresh access token when expired (`/token/refresh/`)

