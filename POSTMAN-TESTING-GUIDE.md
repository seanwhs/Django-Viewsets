# Postman Testing Guide – DRF ViewSets Project

This guide shows how to test the **Contacts** and **Products** APIs using **Postman**, including **JWT authentication** for protected endpoints.

---

## 1. Setup Postman

1. Download and install [Postman](https://www.postman.com/downloads/).
2. Open Postman and create a **new collection** called `DRF ViewSets Project`.
3. Set a **base URL variable** in your collection:

```
Key: base_url
Value: http://127.0.0.1:8000/api
```

This allows you to use `{{base_url}}/products/` and `{{base_url}}/contacts/` in requests.

---

## 2. Test Public Products Endpoint

**Endpoint:** List all products (no authentication required)

1. Create a **GET request** in Postman.
2. URL:

```
{{base_url}}/products/
```

3. No headers or body required.
4. Click **Send** → you should see a JSON array of products (empty if none created yet).

✅ This endpoint is **public**—no JWT required.

---

## 3. Obtain JWT Tokens

**Endpoint:** `/api/token/` (POST)

1. Create a **POST request** in Postman.
2. URL:

```
{{base_url}}/token/
```

3. Set **Body → raw → JSON**:

```json
{
  "username": "your_superuser_username",
  "password": "your_superuser_password"
}
```

4. Click **Send** → JSON response:

```json
{
  "access": "<your-access-token>",
  "refresh": "<your-refresh-token>"
}
```

5. Copy the `access` token to use for protected endpoints.

---

## 4. Use JWT Token in Postman

1. Select your **collection** or **individual request**.

2. Go to the **Authorization** tab:

   * Type: **Bearer Token**
   * Token: Paste your `access` token

3. All requests marked as **JWT required** must include this token.

💡 Tip: You can also set an **environment variable** for `access_token` and reference it with `{{access_token}}`.

---

## 5. Test Protected Products Endpoints

All endpoints except `list` require JWT.

### Create a Product

* Method: **POST**
* URL:

```
{{base_url}}/products/
```

* Body → raw → JSON:

```json
{
  "slug": "test-product",
  "name": "Test Product",
  "price": 100
}
```

* Header: Authorization → Bearer `<access-token>`
* Click **Send** → Response: **201 Created**

---

### Retrieve a Product by Slug

* Method: **GET**
* URL:

```
{{base_url}}/products/test-product/
```

* Header: Authorization → Bearer `<access-token>`
* Click **Send** → JSON of product is returned.

---

### Update a Product (Full)

* Method: **PUT**
* URL:

```
{{base_url}}/products/test-product/
```

* Body → raw → JSON:

```json
{
  "slug": "test-product",
  "name": "Updated Product",
  "price": 120
}
```

* Header: Authorization → Bearer `<access-token>`
* Click **Send** → JSON of updated product.

---

### Partial Update a Product

* Method: **PATCH**
* URL:

```
{{base_url}}/products/test-product/
```

* Body → raw → JSON (only fields to update):

```json
{
  "price": 150
}
```

* Header: Authorization → Bearer `<access-token>`
* Click **Send** → JSON of updated product.

---

### Delete a Product

* Method: **DELETE**
* URL:

```
{{base_url}}/products/test-product/
```

* Header: Authorization → Bearer `<access-token>`
* Click **Send** → Response: **204 No Content**

---

## 6. Test Contacts Endpoints

All **contacts endpoints require JWT**.

### List Contacts

* Method: **GET**
* URL:

```
{{base_url}}/contacts/
```

* Header: Authorization → Bearer `<access-token>`
* Send → JSON array of contacts.

---

### Create Contact

* Method: **POST**
* URL:

```
{{base_url}}/contacts/
```

* Body → raw → JSON:

```json
{
  "fname": "John",
  "lname": "Doe"
}
```

* Header: Authorization → Bearer `<access-token>`
* Send → JSON of created contact.

---

### Retrieve / Update / Delete Contact

* Use `/api/contacts/<id>/`
* Include **Bearer token** in Authorization header
* Methods: **GET**, **PUT**, **PATCH**, **DELETE**

---

## 7. Refresh JWT Token

**Endpoint:** `/api/token/refresh/` (POST)

1. Method: **POST**
2. URL:

```
{{base_url}}/token/refresh/
```

3. Body → raw → JSON:

```json
{
  "refresh": "<your-refresh-token>"
}
```

4. Click **Send** → new `access` token returned.

💡 Use this token for subsequent requests without logging in again.

---

## 8. Quick Tips

* Use **environment variables** for `base_url`, `access_token`, and `refresh_token`.
* Save all requests in the collection for easy retesting.
* Remember:

  * `/products/` → list is **public**
  * `/products/<slug>/` → **JWT required**
  * `/contacts/` → **all JWT protected**

---

✅ **This guide gives a full Postman workflow**:

1. Obtain JWT tokens
2. Test public endpoints (`GET /products/`)
3. Test JWT-protected endpoints with Bearer token
4. Refresh tokens when needed

