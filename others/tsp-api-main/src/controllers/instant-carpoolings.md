# TSP API Instant Carpoolings Controller Documentation

## 🔍 Quick Summary (TL;DR)
The instant carpoolings controller manages real-time carpool matching and ride coordination, enabling users to create, join, and manage spontaneous carpool trips with CRUD operations and workflow management.

**Keywords:** instant-carpooling | real-time-rideshare | carpool-matching | ride-coordination | trip-management | peer-to-peer-transport | dynamic-rideshare | on-demand-carpool

**Primary use cases:** Creating instant carpool offers, joining available rides, managing carpool lifecycle, tracking ride history

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I create an instant carpool?** → [Create Carpool](#create-instant-carpool-post-)
- **Q: How can I join someone's carpool?** → [Join Carpool](#join-carpool-patch-idjoin)
- **Q: What happens when a ride starts?** → [Start Ride](#start-ride-patch-idstart)
- **Q: How do I view my carpool history?** → [Get History](#get-history-get-history)
- **Q: Can I leave a carpool after joining?** → [Leave Carpool](#leave-carpool-patch-idleave)
- **Q: How does timezone handling work?** → Uses 'America/Chicago' as default timezone
- **Q: What authentication is required?** → JWT authentication with userid header

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital bulletin board for spontaneous ride sharing**. Users can post "I'm driving to downtown in 20 minutes, anyone need a ride?" or browse available rides and hop in. The system manages the entire journey from posting the offer, matching with riders, coordinating the actual trip, and handling feedback afterward - like a real-time ride-sharing coordinator.

**Technical explanation:** 
A comprehensive Koa.js REST controller providing full CRUD operations for instant carpool management. It handles the complete lifecycle from creation to completion, including real-time coordination features like joining, leaving, starting, and finishing rides. All operations are user-scoped and include timezone-aware scheduling.

**Business value explanation:**
Enables efficient real-time ridesharing that reduces traffic congestion, lowers transportation costs, and builds community connections. Critical for urban mobility solutions and corporate transportation programs.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/instant-carpoolings.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** CRUD REST Controller
- **File Size:** ~4.2 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Multiple workflow endpoints with state management)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/schemas/instant-carpoolings`: Input validation schemas (**Critical**)
- `@app/src/services/instant-carpoolings`: Business logic service layer (**Critical**)

## 📝 Detailed Code Analysis

### Main Endpoints

#### Create Instant Carpool (`POST /`)
Creates new carpool offers with driver details, route, and timing.

#### Get History (`GET /history`)
Retrieves user's carpool participation history with filtering options.

#### Get Carpool Details (`GET /:id`)
Fetches specific carpool information including current participants.

#### Delete Carpool (`DELETE /:id`)
Removes carpool offers (typically only available to creators).

#### Join Carpool (`PATCH /:id/join`)
Allows users to join available carpool rides with timezone handling.

#### Leave Carpool (`PATCH /:id/leave`)
Enables participants to exit carpools before trip starts.

#### Start Ride (`PATCH /:id/start`)
Initiates the actual carpool trip, transitioning from planning to active state.

#### Finish Ride (`PATCH /:id/finish`)
Completes carpool trips and enables post-trip activities.

#### Add Comments (`PATCH /:id/comment`)
Allows participants to provide feedback and ratings after completion.

### Key Features
- **User Scoping:** All operations tied to authenticated user via userid header
- **Timezone Support:** Configurable timezone with 'America/Chicago' default
- **State Management:** Workflow transitions from creation → joining → active → completed
- **Validation:** Comprehensive input validation for all operations

## 🚀 Usage Methods

### Create Instant Carpool
```bash
curl -X POST "https://api.tsp.example.com/api/v2/instant_carpoolings" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "29.7604,-95.3698",
    "destination": "29.7749,-95.3628",
    "departure_time": "2024-06-25T15:30:00Z",
    "available_seats": 3,
    "notes": "Going to downtown, welcome to join!"
  }'
```

### Join Available Carpool
```bash
curl -X PATCH "https://api.tsp.example.com/api/v2/instant_carpoolings/123/join" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_67890" \
  -H "zone: America/Chicago"
```

### Get Carpool History
```bash
curl -X GET "https://api.tsp.example.com/api/v2/instant_carpoolings/history?page=1&limit=10" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Start Ride
```bash
curl -X PATCH "https://api.tsp.example.com/api/v2/instant_carpoolings/123/start" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "zone: America/Chicago" \
  -H "Content-Type: application/json" \
  -d '{
    "actual_start_time": "2024-06-25T15:35:00Z"
  }'
```

## 📊 Output Examples

### Successful Carpool Creation
```json
{
  "result": "success",
  "data": {
    "id": 123,
    "driver_id": "usr_12345",
    "origin": "29.7604,-95.3698",
    "destination": "29.7749,-95.3628",
    "departure_time": "2024-06-25T15:30:00Z",
    "available_seats": 3,
    "current_passengers": 0,
    "status": "active",
    "created_at": "2024-06-25T14:30:00Z"
  }
}
```

### Join Carpool Response
```json
{
  "result": "success",
  "data": {
    "carpool_id": 123,
    "participant_id": "usr_67890",
    "joined_at": "2024-06-25T14:45:00Z",
    "status": "confirmed"
  }
}
```

### History Response
```json
{
  "result": "success",
  "data": {
    "carpools": [
      {
        "id": 123,
        "role": "driver",
        "origin": "Downtown",
        "destination": "Airport",
        "date": "2024-06-25",
        "status": "completed",
        "participants": 2
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 15
    }
  }
}
```

## ⚠️ Important Notes

### Workflow States
- **Created:** Carpool offer posted, accepting participants
- **Active:** Trip in progress
- **Completed:** Trip finished, ready for feedback
- **Cancelled:** Trip cancelled before completion

### Timezone Handling
- Default timezone: 'America/Chicago'
- Configurable via 'zone' header
- Critical for departure time coordination

### Security Features
- JWT authentication required for all endpoints
- User-scoped operations prevent unauthorized access
- Input validation prevents malformed requests

### Business Rules
- Drivers can manage their own carpools
- Passengers can join/leave before trip starts
- Comments only allowed after completion
- Seat availability managed automatically

## 🔗 Related File Links

- **Service Layer:** `allrepo/connectsmart/tsp-api/src/services/instant-carpoolings.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/instant-carpoolings.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This controller provides essential real-time carpool coordination functionality for dynamic ridesharing services.*