# TSP API Calendar Events Controller Documentation

## 🔍 Quick Summary (TL;DR)
The calendar events controller provides CRUD (Create, Update, Delete) endpoints for managing user-specific calendar events within the TSP API ecosystem.

**Keywords:** calendar-events | user-events | schedule | event-management | tsp-api | crud-api | koa-router | rest-api

**Primary use cases:** Syncing user calendar data from a mobile app, allowing users to create personal travel-related events, updating event details, deleting events from a user's calendar.

**Compatibility:** Node.js >=16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I create new calendar events?** → [Create Calendar Events](#create-calendar-events-post-)
- **Q: How do I update an existing event?** → [Update a Calendar Event](#update-a-calendar-event-put-id)
- **Q: How do I delete a calendar event?** → [Delete a Calendar Event](#delete-a-calendar-event-delete-id)
- **Q: What data format is expected when creating events?** → [Input Validation Schemas](#input-validation-schemas)
- **Q: What authentication is needed for these operations?** → [Authentication and Authorization](#authentication-and-authorization)
- **Q: What is the `userid` header for?** → [Header Requirements](#header-requirements)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **personal assistant for your travel schedule**. You can give the assistant a list of new appointments (`POST`), and they'll add them to your calendar. You can hand them an updated invitation with a new time or location (`PUT`), and they'll revise the correct entry. Or you can tell them to cross an event off your schedule entirely (`DELETE`). The assistant always checks your ID (`auth` middleware) before making any changes to ensure it's your calendar they're managing.

**Technical explanation:** 
A standard Koa.js REST controller that exposes `POST`, `PUT`, and `DELETE` endpoints for full CRUD functionality on a user's calendar events. All endpoints are protected by JWT authentication via middleware. It uses Joi for rigorous input validation on both the request body and URL parameters. The controller acts as a thin routing layer, delegating all business logic to the `calendar-events` service layer.

**Business value explanation:**
This controller enables features that increase user engagement and personalization. By allowing users to manage their travel-related events within the application, the platform can provide more contextual and timely services, such as departure reminders, route planning suggestions for upcoming trips, and integration with other MaaS features.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/calendar-events.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~1.5 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - Standard CRUD with validation and service delegation)

**Dependencies (Criticality Level):**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized success/error response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/schemas/calendar-events`: Joi validation schemas for input (**Critical**)
- `@app/src/services/calendar-events`: Business logic service layer (**Critical**)

### Header Requirements
- `Authorization`: (Required) The Bearer token for authentication. Example: `Bearer eyJhbGci...`
- `userid`: (Required) The public ID of the user performing the action. This is used by the service layer to associate the event with the correct user. Example: `usr_...`

## 📝 Detailed Code Analysis

### Endpoint Signatures & Flow

#### Create Calendar Events (`POST /`)
- **Signature:** `router.post('createCalendarEvents', '/', auth, bodyParser(), async (ctx) => { ... })`
- **Flow:**
    1. `auth` middleware verifies JWT token.
    2. `bodyParser` parses the request body.
    3. The `userid` is extracted from the request header.
    4. The request body is validated against the `inputValidator.create` schema. This expects an object with an `events` array.
    5. The validated `events` array and the `userId` are passed to `service.create()`.
    6. The result from the service is returned in a standard success response.

#### Update a Calendar Event (`PUT /:id`)
- **Signature:** `router.put('updateCalendarEvent', '/:id', auth, bodyParser(), async (ctx) => { ... })`
- **Flow:**
    1. Authentication and body parsing occur.
    2. `userid` is extracted from the header.
    3. The event `id` (UUID) is extracted from the URL parameters (`ctx.params`).
    4. The `id` and the request body are combined and validated against the `inputValidator.update` schema.
    5. The validated data, along with the `userId`, is passed to `service.update()`.
    6. The service's result is returned in the response.

#### Delete a Calendar Event (`DELETE /:id`)
- **Signature:** `router.delete('deleteCalendarEvent', '/:id', auth, bodyParser(), async (ctx) => { ... })`
- **Flow:**
    1. Authentication and body parsing occur.
    2. `userid` is extracted from the header.
    3. The `id` from the URL parameters is validated against the `inputValidator.pathParams` schema.
    4. An input object containing the event `uuid` and the `userId` is passed to `service.delete()`. This ensures a user can only delete their own events.
    5. The result is returned in the response.

### Design Patterns
- **Thin Controller:** The controller is "thin" because it contains minimal business logic. Its main responsibilities are routing, authentication, and input validation. All the complex work of interacting with the database is delegated to the service layer, promoting separation of concerns.
- **Validation-First:** Each endpoint validates all incoming data before passing it to the service layer, preventing invalid data from reaching the core business logic.

## 🚀 Usage Methods

### Create Events (`POST /api/v2/calendar_events`)
```bash
curl -X POST "https://api.tsp.example.com/api/v2/calendar_events" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "uuid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "title": "Meeting with Client",
        "startTime": "2024-09-15T09:00:00.000Z",
        "endTime": "2024-09-15T10:00:00.000Z",
        "location": "123 Main St, Anytown, USA"
      }
    ]
  }'
```

### Update an Event (`PUT /api/v2/calendar_events/:id`)
```bash
curl -X PUT "https://api.tsp.example.com/api/v2/calendar_events/a1b2c3d4-e5f6-7890-1234-567890abcdef" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Meeting with Client",
    "endTime": "2024-09-15T10:30:00.000Z"
  }'
```

### Delete an Event (`DELETE /api/v2/calendar_events/:id`)
```bash
curl -X DELETE "https://api.tsp.example.com/api/v2/calendar_events/a1b2c3d4-e5f6-7890-1234-567890abcdef" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: usr_12345"
```

## 📊 Output Examples

### Successful Response (Create/Update/Delete)
A successful operation will return an HTTP 200 status code with a body containing the result from the service layer, which might be the created/updated record or a confirmation status.

```json
{
  "result": "success",
  "data": {
    "uuid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "title": "Updated Meeting with Client",
    "startTime": "2024-09-15T09:00:00.000Z",
    "endTime": "2024-09-15T10:30:00.000Z",
    "userId": "usr_12345"
  }
}
```

### Validation Error Response (400)
If the input data does not match the schema (e.g., a required field is missing):

```json
{
  "error": "ValidationError",
  "message": "\"events[0].title\" is required",
  "details": [
    {
      "message": "\"events[0].title\" is required",
      "path": [
        "events",
        0,
        "title"
      ],
      "type": "any.required"
    }
  ]
}
```

## 🔗 Related File Links

- **Input Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/calendar-events.js`
- **Business Logic Service:** `allrepo/connectsmart/tsp-api/src/services/calendar-events.js`
- **Authentication Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was generated based on the provided template and source file.*
