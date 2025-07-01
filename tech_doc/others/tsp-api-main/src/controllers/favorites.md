# Favorites Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller provides a standard suite of CRUD (Create, Read, Update, Delete) endpoints for managing a user's saved favorite locations, such as "Home," "Work," or other frequently used places.

**Keywords:** favorites | saved-places | locations | crud-api | user-preferences | tsp-api | koa-router | home-work-address

**Primary use cases:** 
- Retrieving a user's list of saved favorite locations.
- Adding a new favorite location.
- Updating the details of an existing favorite location (e.g., renaming "Home").
- Deleting a saved favorite location.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I get all of a user's favorites?** → [GET /](#get-)
- **Q: How do I save a new favorite place?** → [POST /](#post-)
- **Q: How do I change the name or address of a favorite?** → [PUT /:id](#put-id)
- **Q: How do I remove a favorite?** → [DELETE /:id](#delete-id)
- **Q: What authentication is required?** → All endpoints require JWT authentication.
- **Q: How is the user identified for their favorites?** → Via the `userid` in the JWT token passed in the header.
- **Q: Why does the `PUT` endpoint manually list parameters?** → To work around an issue with the Android client sending extra, undefined parameters.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as the manager of your GPS or map app's "Saved Places" list. It lets you see all your saved places like "Home" and "Work" (`GET`), add a new place like "Mom's House" (`POST`), edit a saved place if you move or want to rename it (`PUT`), and remove a place you no longer visit (`DELETE`). It's the core functionality for personalizing the map experience with your most important locations.

**Technical explanation:** 
A standard Koa.js REST controller that exposes the four CRUD verbs (`GET`, `POST`, `PUT`, `DELETE`) on the `/api/v1/favorites` resource. All endpoints are protected by JWT `auth` middleware. The controller is a thin routing layer that validates incoming data against Joi schemas and delegates the business logic to either the `Favorites` model (for simple queries like `GET`) or the `favorites` service (for more complex operations like `create`, `update`, `delete`). A notable feature is the workaround in the `PUT` endpoint to strip extraneous parameters sent by a specific client before validation.

**Business value explanation:**
Saving favorite locations is a fundamental feature for any transportation or mapping application. It dramatically improves usability by allowing users to select common origins and destinations with a single tap instead of typing them out repeatedly. This increases user satisfaction, reduces friction in trip planning, and provides valuable (anonymized) data on key locations, which can be used to improve service offerings.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/favorites.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API CRUD Controller
- **File Size:** ~2 KB
- **Complexity Score:** ⭐⭐ (Low - A standard CRUD implementation with a minor client-specific workaround.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@maas/core/response`: Standardized success response formatter (**High**).
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**).
- `@app/src/helpers/fields-of-header`: Utility to extract user context from headers (**High**).
- `@app/src/schemas/favorites`: Joi schemas for input validation (**Critical**).
- `@app/src/models/Favorites`: The Bookshelf/Knex model for direct database interaction (**Critical**).
- `@app/src/services/favorites`: The service layer for business logic (**Critical**).

## 📝 Detailed Code Analysis

### `GET /`
- **Purpose**: Retrieve all favorite locations for the authenticated user.
- **Logic**: This endpoint uses the `Favorites` model directly for a simple `query().where('user_id', userId)`. This is efficient as it doesn't require complex business logic that would necessitate a service layer call.

### `POST /`
- **Purpose**: Create a new favorite location.
- **Logic**: Follows the standard pattern: validate combined header/body input, then delegate to `services.create(input)`.

### `PUT /:id`
- **Purpose**: Update a specific favorite location, identified by its `id`.
- **Logic**: This endpoint contains a specific workaround.
    1. It manually creates a `queryParam` object, cherry-picking only the expected fields from the `ctx.request.body`.
    2. The comment explicitly states this is to accommodate an Android client that sends extra, undefined parameters which would cause Joi validation to fail.
    3. This "sanitized" `queryParam` object is then combined with header and URL parameter data for validation before being passed to `services.update(input)`. This is a pragmatic solution to a client-side issue.

### `DELETE /:id`
- **Purpose**: Remove a favorite location by its `id`.
- **Logic**: Follows the standard pattern: validate header/URL params, then delegate to `services.delete(input)`.

## 🚀 Usage Methods

**Base URL:** `https://api.tsp.example.com/api/v1/favorites`
**Headers (for all requests):**
- `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- `userid`: `usr_...` (The user's ID)
- `Content-Type`: `application/json` (for POST/PUT)

### Get All Favorites
```bash
curl -X GET "https://api.tsp.example.com/api/v1/favorites" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123"
```

### Create a New Favorite
```bash
curl -X POST "https://api.tsp.example.com/api/v1/favorites" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Home",
    "address": "123 Main St, Houston, TX",
    "latitude": 29.7604,
    "longitude": -95.3698,
    "category": "home",
    "icon_type": "home"
  }'
```

### Update a Favorite
```bash
curl -X PUT "https://api.tsp.example.com/api/v1/favorites/fav_abcde" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Work Office"
  }'
```

### Delete a Favorite
```bash
curl -X DELETE "https://api.tsp.example.com/api/v1/favorites/fav_abcde" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123"
```

## 📊 Output Examples

### Successful GET Response
```json
{
  "result": "success",
  "data": {
    "favorites": [
      { "id": "fav_home", "user_id": "usr_123", "name": "Home", ... },
      { "id": "fav_work", "user_id": "usr_123", "name": "Work", ... }
    ]
  }
}
```

### Successful POST/PUT Response
```json
{
  "result": "success",
  "data": {
    "id": "fav_home",
    "user_id": "usr_123",
    "name": "Home",
    "address": "123 Main St, Houston, TX",
    ...
  }
}
```

### Validation Error Response (400)
If a required field is missing from a `POST` request:
```json
{
    "error": "ERROR_BAD_REQUEST_BODY",
    "message": "\"name\" is required",
    "code": 400
}
```

## ⚠️ Important Notes
- **Client-Specific Workaround**: The `PUT` endpoint's logic is a point of technical debt. While it solves the immediate problem with the Android client, the ideal solution would be for the client to send a clean request body. This workaround could be confusing for future developers if not for the explanatory comment.
- **User-Centric**: All operations are implicitly scoped to the `userId` from the authenticated session, ensuring users can only manage their own favorites.

## 🔗 Related File Links
- **Business Logic Service:** `allrepo/connectsmart/tsp-api/src/services/favorites.js`
- **Database Model:** `allrepo/connectsmart/tsp-api/src/models/Favorites.js`
- **Input Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/favorites.js`
- **Authentication Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was regenerated to provide a more comprehensive, structured overview of this standard CRUD controller and to highlight its client-specific workaround.*
