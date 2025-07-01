# TSP API Carpool Controller Documentation

## 🔍 Quick Summary (TL;DR)
The carpool controller manages carpooling reservations, handling creation, cancellation, and providing suggested pricing based on trip details.

**Keywords:** carpool | ride-sharing | reservation | transportation | tsp-api | koa-router | matching-engine | suggested-price

**Primary use cases:** Creating a carpool request, matching drivers and riders, canceling a carpool reservation, calculating a fair price for a carpool trip.

**Compatibility:** Node.js >=16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I create a carpool ride request?** → [Create a Carpool](#create-a-carpool-post-v1carpool)
- **Q: How do I cancel an existing carpool?** → [Cancel a Carpool](#cancel-a-carpool-delete-v2carpoolreservationidreason)
- **Q: How is the suggested price for a trip calculated?** → [Get Suggested Price](#get-suggested-price-get-v1suggested_price)
- **Q: What happens if my carpool request conflicts with another reservation?** → [Conflict Handling](#conflict-handling)
- **Q: What is the `cancelCarpool` function inside the controller file?** → [Internal Helper Function](#internal-helper-function-cancelcarpool)
- **Q: Why does the create endpoint return a `security_key`?** → [Security Key](#security-key)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **carpool coordinator**. You submit a ride request with your origin, destination, and schedule (`POST /v1/carpool`). The coordinator checks its board for potential matches and tries to set you up with a driver or rider. If it finds a match, it confirms the ride. If you need to cancel, you call the coordinator and give them your reservation number and a reason (`DELETE /v2/carpool/...`). It also has a "fare calculator" that can give you a price estimate for a potential trip before you even book (`GET /v1/suggested_price`).

**Technical explanation:** 
A Koa.js REST controller that exposes endpoints for managing the carpool lifecycle. The `POST /v1/carpool` endpoint validates user input and invokes a service to create a reservation, which may also trigger a matching process. It handles potential scheduling conflicts by returning a specific conflict response. The `DELETE /v2/carpool/:reservationId/:reason` endpoint cancels a reservation. An unauthenticated `GET /v1/suggested_price` endpoint provides pricing information. The controller interfaces with the `carpool` service for business logic and the `AuthUsers` model to retrieve user-specific data like the `security_key`.

**Business value explanation:**
This controller is fundamental to the carpooling feature of the MaaS platform. It enables users to find and share rides, reducing traffic congestion and transportation costs. The matching logic helps increase vehicle occupancy, and the suggested price feature provides transparency and builds user trust.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/carpool.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **Complexity Score:** ⭐⭐⭐ (Medium - involves complex service-layer interactions and specific business logic for creation and cancellation)

**Dependencies (Criticality Level):**
- `koa-body`: Request body parsing (**Critical**)
- `@koa/router`: HTTP routing framework (**Critical**)
- `@maas/core/response`: Standardized success/error response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/services/carpool`: Core carpool business logic service (**Critical**)
- `@app/src/schemas/carpool`: Joi validation schemas for input (**Critical**)
- `@app/src/helpers/fields-of-header`: Utility for extracting data from headers (**High**)
- `@app/src/models/AuthUsers`: Database model for user data (**Critical**)

## 📝 Detailed Code Analysis

### Endpoint Signatures & Flow

#### Create a Carpool (`POST /v1/carpool`)
- **Signature:** `router.post('createCarpool', '/v1/carpool', auth, bodyParser(), async (ctx) => { ... })`
- **Flow:**
    1.  Authenticates the user and parses the request body.
    2.  Validates input from headers and body against the `createCarpool` schema.
    3.  Calls `service.createCarpool(input)`. This service method is expected to return an array `[createData, matchData, conflict]`.
    4.  **Conflict Handling:** If the `conflict` variable is truthy, it immediately returns a success response containing the ID of the conflicting reservation.
    5.  If there is no conflict, it fetches the user's profile from the `AuthUsers` model to retrieve their `security_key`.
    6.  It returns a success response containing the created reservation data, any immediate match data, and the user's `security_key`.
    7.  Includes a `try...catch` block for detailed error logging.

#### Cancel a Carpool (`DELETE /v2/carpool/:reservationId/:reason`)
- **Signature:** `router.delete('cancelCarpool', '/v2/carpool/:reservationId/:reason', auth, bodyParser(), cancelCarpool)`
- **Flow:**
    - This endpoint is interesting because it delegates its entire logic to the internal `cancelCarpool` helper function defined within the same file.
    - The `cancelCarpool` function extracts the `userId`, `reservationId`, and `reason` and passes them to `service.cancelCarpool(data)`.
    - It includes a `@todo` comment indicating that Joi validation is required before production use.

#### Get Suggested Price (`GET /v1/suggested_price`)
- **Signature:** `router.get('getSuggestedPrice', '/v1/suggested_price', bodyParser(), async (ctx) => { ... })`
- **Flow:**
    - This endpoint is **not authenticated** via the `auth` middleware.
    - It validates query parameters using the `getSuggestedPrice` schema.
    - It calls `service.getSuggestedPrice(input)` to perform the calculation.
    - It returns the result from the service.

### Internal Helper Function (`cancelCarpool`)
The controller defines a local `async function cancelCarpool(ctx)`. This function contains the logic for the DELETE endpoint. While this works, it's a slightly unconventional pattern. Typically, this logic would either be directly inside the router handler lambda `async (ctx) => { ... }` or, if reused, in a separate helper file. Its existence here, along with the `@todo` for validation, suggests it might be for testing or a feature under development.

## 🚀 Usage Methods

### Create a Carpool Request
```bash
curl -X POST "https://api.tsp.example.com/api/v1/carpool" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: 12345" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": { "lat": 29.76, "lon": -95.36 },
    "destination": { "lat": 29.74, "lon": -95.38 },
    "departureTime": "2024-10-01T08:00:00Z",
    "role": "rider"
  }'
```

### Cancel a Carpool Reservation
```bash
curl -X DELETE "https://api.tsp.example.com/api/v2/carpool/res_abc123/user_cancelled" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: 12345"
```

### Get a Suggested Price
```bash
curl -X GET "https://api.tsp.example.com/api/v1/suggested_price?distance=15000&duration=1800"
```

## 📊 Output Examples

### Successful Carpool Creation (No Immediate Match)
```json
{
  "result": "success",
  "data": {
    "create": {
      "reservationId": "res_def456",
      "status": "pending"
    },
    "match": null,
    "security_key": "sk_user_secret_key"
  }
}
```

### Carpool Creation with Scheduling Conflict
```json
{
  "result": "success",
  "data": {
    "conflict_reservation_id": "res_xyz789"
  }
}
```

### Successful Cancellation
```json
{
  "result": "success",
  "data": {}
}
```

## 🔗 Related File Links

- **Input Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/carpool.js`
- **Business Logic Service:** `allrepo/connectsmart/tsp-api/src/services/carpool.js`
- **User Data Model:** `allrepo/connectsmart/tsp-api/src/models/AuthUsers.js`
- **Authentication Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was generated based on the provided template and source file.*
