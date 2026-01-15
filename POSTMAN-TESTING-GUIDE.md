# Postman Testing Guide – DRF ViewSets Project

This guide shows how to test the **Contacts** and **Products** APIs using **Postman**, including **JWT authentication** for protected actions.

---

## 1. Setup Postman

1. Download and install [Postman](https://www.postman.com/downloads/) if you don’t have it already.
2. Open Postman and create a **new collection** called `DRF ViewSets Project`.
3. Set a **base URL variable** in your collection:

```
Key: base_url
Value: http://127.0.0.1:8000/api
```

This makes testing easier (e.g., `{{base_url}}/products/`).

---

## 2. Test Public Products Endpoint

**Endpoint:** List all products (no authentication required)

1. Create a new **GET request** in Postman.
2. URL:

```
{{base_url}}/products/
```

3. No headers or body required.
4. Click **Send** → You should see a JSON array of products (empty if none created yet).

✅ This endpoint is **public**, so no JWT is needed.

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

4. Click **Send** → You will receive a JSON response:

```json
{
  "access": "<your-access-token>",
  "refresh": "<your-refresh-token>"
}
```

5. Copy the `access` token – you will use it for protected endpoints.

---

## 4. Use JWT Token in Postman

1. In Postman, select your **collection** or **individual request**.
2. Go to the **Authorization tab**:

   * Type: **Bearer Token**
   * Token: Paste your `access` token
3. All requests with **JWT required** must include this token.

---

## 5. Test Protected Products Endpoints

All endpoints except `list` require JWT.

### Example: Create a Product

1. Method: **POST**
2. URL:

```
{{base_url}}/products/
```

3. Headers: Authorization → Bearer `<access-token>`
4. Body → raw → JSON:

```json
{
  "slug": "test-product",
  "name": "Test Product",
  "price": 100
}
```

5. Click **Send** → You should get **201 Created** with the product JSON.

---

### Example: Retrieve a Product by Slug

1. Method: **GET**
2. URL:

```
{{base_url}}/products/test-product/
```

3. Header: Authorization → Bearer `<access-token>`
4. Send → JSON of product is returned.

---

### Example: Update a Product

1. Method: **PUT**
2. URL:

```
{{base_url}}/products/test-product/
```

3. Header: Authorization → Bearer `<access-token>`
4. Body → raw → JSON (full update):

```json
{
  "slug": "test-product",
  "name": "Updated Product",
  "price": 120
}
```

5. Send → JSON of updated product.

---

### Example: Delete a Product

1. Method: **DELETE**
2. URL:

```
{{base_url}}/products/test-product/
```

3. Header: Authorization → Bearer `<access-token>`
4. Send → Response **204 No Content**.

---

## 6. Test Contacts Endpoints

All **contacts endpoints require JWT**.

### Example: List Contacts

1. Method: **GET**
2. URL:

```
{{base_url}}/contacts/
```

3. Header: Authorization → Bearer `<access-token>`
4. Send → JSON array of contacts.

### Example: Create Contact

1. Method: **POST**
2. URL:

```
{{base_url}}/contacts/
```

3. Header: Authorization → Bearer `<access-token>`
4. Body → raw → JSON:

```json
{
  "fname": "John",
  "lname": "Doe"
}
```

5. Send → JSON of created contact.

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

4. Send → You get a new `access` token to continue making requests.

---

## 8. Tips

* Use **Postman Environment Variables** for base URL and JWT tokens to make testing easier.
* You can **save requests in the collection** to quickly test all endpoints.
* Remember:

  * `/products/` → `list` is public
  * All other endpoints → JWT required
  * All `/contacts/` endpoints → JWT required

---

This guide gives you a **full workflow**:

1. Get JWT tokens
2. Test public endpoints
3. Test protected endpoints with Bearer token
4. Refresh tokens when expired

