# Trip Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller manages the entire lifecycle of a user's trip, from creation ("start trip") to completion ("end trip"). It also provides endpoints for fetching trip history, trip counts, detailed information about a specific trip, and managing trip validation statuses (particularly for payments).

**Keywords:** trip | trip-lifecycle | trip-history | trip-planning | start-trip | end-trip | trip-status | tsp-api

**Primary use cases:** 
- Starting a new trip record when a user begins a journey.
- Ending a trip record upon arrival, which may trigger fare calculation.
- Retrieving a paginated list of a user's past trips.
- Getting the total count of a user's trips, filterable by date and mode.
- Fetching the detailed itinerary and data for a single past trip.
- Getting and setting the payment/validation status for a trip, crucial for features like DUO carpooling.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I start a new trip?** → [POST /v1/trip](#post-v1trip)
- **Q: How do I end a trip?** → [PUT /v1/trip/:tripId](#put-v1triptripid)
- **Q: How can I get a user's trip history?** → [GET /v2/trips](#get-v2trips)
- **Q: What is `trip_status` used for?** → It's used to check and update the payment and validation status of a trip, which is especially important for post-trip billing or validation schemes.
- **Q: How is this different from `routing.js`?** → `routing.js` plans a *future* trip. `trip.js` records and manages an *active or past* trip.
- **Q: How does pagination work for trip history?** → The `GET /v2/trips` endpoint likely supports `offset` and `limit` parameters passed through the `getTrips` schema.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **vehicle's trip odometer and logbook manager**.
- **Starting a Journey (`POST /v1/trip`):** When you start driving, you press the "Trip" button. The manager records your starting point, time, and planned route, and gives you a new trip ID.
- **Ending a Journey (`PUT /v1/trip/:tripId`):** When you arrive, you press the button again. The manager logs your end time and location, calculates the final details, and closes the log entry.
- **Reviewing the Logbook (`GET /v2/trips`, `GET /v2/trip_details`):** At any time, you can ask the manager to show you a list of all your past trips, or to pull up the detailed page for a specific journey.
- **Checking the Tolls (`GET /v2/trip_status`):** For special trips (like a carpool), you can ask the manager if the toll has been paid and validated. If you're the toll operator, you can tell the manager to mark the trip as "paid" (`POST /v2/trip_status`).
- **Counting Your Trips (`GET /v2/trip_count`):** You can ask the manager for a summary, like "How many trips did I take last month by bike?"

**Technical explanation:** 
A comprehensive Koa.js REST controller for managing the full lifecycle of trip entities. It exposes a mix of v1 and v2 endpoints. The v1 endpoints (`/v1/trip`) handle the state changes of a trip (starting and ending). The v2 endpoints provide extensive capabilities for querying trip data, including paginated history (`/v2/trips`), aggregate counts (`/v2/trip_count`), and detailed lookups (`/v2/trip_details`). A distinct `trip_status` resource provides getter and setter methods to manage payment and validation states asynchronously from the trip itself. The controller consistently uses Joi for validation and delegates all business logic to a corresponding function in the `trip` service.

**Business value explanation:**
This controller is fundamental to the entire application, as it creates and manages the core data entity: the trip. Accurate trip logging is essential for a vast range of features, including user behavior analysis, activity history, CO2 savings calculations, incentive programs, and fare collection. The `trip_status` endpoints are particularly vital for enabling complex payment and validation scenarios, such as confirming a shared ride for a corporate subsidy or finalizing payment after a journey, which are key to monetization and partnership integrations.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/trip.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~4 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Manages a core entity with multiple query patterns and state-changing endpoints.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@maas/core/response`: Standardized success response formatter (**High**).
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**).
- `@app/src/helpers/fields-of-header`: Utility to extract user context from headers (**High**).
- `@app/src/schemas/trip`: Joi schemas for input validation (**Critical**).
- `@app/src/services/trip`: The service layer containing all business logic (**Critical**).

## 📝 Detailed Code Analysis

### Trip Lifecycle Endpoints
- **`POST /v1/trip` (`startTrip`)**: Creates a new trip record. It expects a detailed payload with the trip's initial data. It returns a `201 Created` status, which is the correct semantic HTTP response for creating a new resource.
- **`PUT /v1/trip/:tripId` (`endTrip`)**: Updates an existing trip to mark it as complete. It takes the `tripId` from the URL path and updates the record with end-of-trip data (e.g., final location, duration).

### Trip Query Endpoints
- **`GET /v2/trips`**: Fetches a list of trips for the user. It takes filter parameters (like dates and modes) from the query string, validates them, and passes them to the `service.getTrips` function, which handles the database query and pagination.
- **`GET /v2/trip_count`**: Similar to `getTrips`, but it calls a dedicated service function (`service.getTripCount`) that likely performs a more efficient `COUNT(*)` query on the database to return only the total number of trips matching the filters.
- **`GET /v2/trip_details`**: Retrieves all data for a single trip, identified by its ID in the query string.

### Trip Status Endpoints
- **`GET /v2/trip_status`**: A specialized getter that retrieves only the `payment_status` and `validation_status` for a trip. This is a lightweight way to check the status without fetching the entire trip object.
- **`POST /v2/trip_status`**: A specialized setter that allows an authenticated system or user to update the payment status and a reason string for a trip. This is likely used by backend processes after a payment clears or a validation rule is met.

## 🚀 Usage Methods

**Base URL:** `https://api.tsp.example.com`
**Headers:** All requests require `Authorization: Bearer <TOKEN>` and `userid: usr_...`

### Start a Trip
```bash
curl -X POST "https://api.tsp.example.com/api/v1/trip" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{ "mode": "drive", "origin": {...}, "destination": {...} }'
```

### End a Trip
```bash
curl -X PUT "https://api.tsp.example.com/api/v1/trip/trip_abcde" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{ "end_time": "...", "final_polyline": "..." }'
```

### Get Trip History
```bash
curl -X GET "https://api.tsp.example.com/api/v2/trips?offset=0&limit=10" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123"
```

### Get Trip Status
```bash
curl -X GET "https://api.tsp.example.com/api/v2/trip_status?trip_id=trip_abcde" \
  -H "Authorization: Bearer <TOKEN>"
```

## ⚠️ Important Notes
- **API Versioning**: The controller uses two different API versions (`v1` for lifecycle, `v2` for queries). This suggests a historical evolution of the API. While functional, it's something to be aware of for API consistency.
- **Service Layer**: The controller exhibits excellent separation of concerns, with all database interaction and business logic delegated to the `trip` service. The controller is only responsible for routing, authentication, and validation.
- **Error Handling**: The `getTripStatus` endpoint includes explicit checks for the existence of the `tripId` parameter and the resulting database record, throwing specific `MaasError`s for each case, which is a good practice for client-side error handling.

## 🔗 Related File Links
- **Business Logic Service:** `allrepo/connectsmart/tsp-api/src/services/trip.js`
- **Input Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/trip.js`
- **Authentication Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was regenerated to provide a clear and structured overview of the endpoints responsible for managing the complete trip lifecycle.*
