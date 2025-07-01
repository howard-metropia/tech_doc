# TSP API Reservations Controller Documentation

## 🔍 Quick Summary (TL;DR)
The reservations controller manages trip reservations and bookings within the TSP platform, providing functionality to create, retrieve, and view detailed information about user transportation reservations.

**Keywords:** reservations | trip-bookings | travel-reservations | trip-planning | booking-management | transportation-bookings | travel-mode | trip-details

**Primary use cases:** Creating trip reservations, viewing reservation history, getting detailed trip information, managing travel bookings

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I view my reservations?** → [Get Reservations](#get-reservations-get-)
- **Q: How do I create a new reservation?** → [Create Reservation](#create-reservation-post-)
- **Q: How do I get detailed trip information?** → [Get Trip Details](#get-trip-details-get-trip_detailid)
- **Q: Can I filter reservations by travel mode?** → Yes, supports filtering by bus, train, rideshare, etc.
- **Q: How does timezone handling work?** → Uses 'America/Chicago' as default timezone
- **Q: What travel modes are supported?** → All modes defined in Reservations model

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **digital travel booking manager**. Just like how you might book airline tickets or hotel rooms, this controller handles your transportation reservations - whether it's booking a bus seat, reserving a rideshare, or planning a multi-modal trip. You can view all your upcoming and past bookings, create new reservations, and get detailed information about specific trips.

**Technical explanation:** 
A comprehensive Koa.js REST controller that provides full reservation management functionality including retrieval with filtering, creation with timezone handling, and detailed trip information access. It integrates with the reservations model and service layer to handle complex booking scenarios and travel mode management.

**Business value explanation:**
Essential for completing the transportation ecosystem by enabling users to secure their travel plans in advance. Reservations increase user confidence, enable capacity planning for operators, and provide revenue predictability through advance bookings.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/reservations.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Booking/Reservation Management Controller
- **File Size:** ~1.6 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Multiple endpoints with filtering, pagination, and timezone handling)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/schemas/reservations`: Input validation schemas (**Critical**)
- `@app/src/models/Reservations`: Reservations data model (**Critical**)
- `@app/src/services/reservations`: Reservation business logic service (**Critical**)
- `@app/src/static/defines`: Static definitions and constants (**High**)

## 📝 Detailed Code Analysis

### Available Endpoints

#### Get Reservations (`GET /`)
- **Purpose:** Retrieves user's reservations with filtering and pagination
- **Features:** Travel mode filtering, pagination (offset/perpage), today-only filter
- **Default Values:** offset=0, perpage=10, all travel modes included
- **Travel Mode Support:** Supports filtering by multiple travel modes via comma-separated values

#### Create Reservation (`POST /`)
- **Purpose:** Creates new trip reservations with timezone handling
- **Timezone Default:** 'America/Chicago' when not specified in headers
- **Input Processing:** Combines request body with user context and timezone
- **Validation:** Comprehensive validation through reservations schema

#### Get Trip Details (`GET /trip_detail/:id`)
- **Purpose:** Retrieves detailed information for specific reservation
- **Localization:** Supports language-specific responses via locale header
- **Security:** User-scoped access ensuring users only see their own reservations

### Key Features

#### Travel Mode Filtering
```javascript
travelMode: ctx.request.query.travel_mode
  ? ctx.request.query.travel_mode.split(',')
  : Object.values(Reservations.travelMode),
```

#### Timezone Processing
```javascript
const zone = ctx.request.header.zone ?? 'America/Chicago';
const input = { ...ctx.request.body, userId, zone };
```

#### Localization Support
```javascript
const language = defines.language[ctx.request.locale];
```

## 🚀 Usage Methods

### Get User Reservations
```bash
# Basic reservation list
curl -X GET "https://api.tsp.example.com/api/v2/reservation" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"

# Filtered by travel mode with pagination
curl -X GET "https://api.tsp.example.com/api/v2/reservation?travel_mode=bus,train&offset=10&perpage=20&is_today=true" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Create New Reservation
```bash
curl -X POST "https://api.tsp.example.com/api/v2/reservation" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "zone: America/Chicago" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Downtown Station",
    "destination": "Airport Terminal",
    "departure_time": "2024-06-25T15:30:00",
    "travel_mode": "bus",
    "passenger_count": 2,
    "special_requirements": "wheelchair_accessible",
    "contact_info": {
      "phone": "+1-555-123-4567",
      "email": "user@example.com"
    }
  }'
```

### Get Trip Details
```bash
curl -X GET "https://api.tsp.example.com/api/v2/reservation/trip_detail/reservation_123" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Accept-Language: en-US"
```

### JavaScript Client Example
```javascript
async function getReservations(authToken, userId, filters = {}) {
  const params = new URLSearchParams();
  if (filters.travelMode) params.append('travel_mode', filters.travelMode.join(','));
  if (filters.offset) params.append('offset', filters.offset);
  if (filters.perpage) params.append('perpage', filters.perpage);
  if (filters.isToday) params.append('is_today', filters.isToday);
  
  try {
    const response = await fetch(`/api/v2/reservation?${params}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.data;
    }
  } catch (error) {
    console.error('Failed to fetch reservations:', error);
  }
}

async function createReservation(authToken, userId, reservationData, timezone = 'America/Chicago') {
  try {
    const response = await fetch('/api/v2/reservation', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'zone': timezone,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(reservationData)
    });
    
    if (response.ok) {
      const result = await response.json();
      return result.data;
    }
  } catch (error) {
    console.error('Reservation creation failed:', error);
  }
}
```

## 📊 Output Examples

### Reservations List Response
```json
{
  "result": "success",
  "data": {
    "reservations": [
      {
        "id": "reservation_123",
        "origin": "Downtown Station",
        "destination": "Airport Terminal",
        "departure_time": "2024-06-25T15:30:00Z",
        "arrival_time": "2024-06-25T16:45:00Z",
        "travel_mode": "bus",
        "status": "confirmed",
        "passenger_count": 2,
        "total_cost": 24.50,
        "booking_reference": "BUS123456"
      }
    ],
    "pagination": {
      "offset": 0,
      "perpage": 10,
      "total": 25,
      "has_more": true
    }
  }
}
```

### Reservation Creation Response
```json
{
  "result": "success",
  "data": {
    "reservation_id": "reservation_456",
    "booking_reference": "BUS789012",
    "status": "confirmed",
    "departure_time": "2024-06-25T15:30:00Z",
    "confirmation_details": {
      "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSU...",
      "confirmation_number": "CONF789012",
      "cancellation_policy": "Free cancellation up to 2 hours before departure"
    },
    "total_cost": 24.50,
    "payment_status": "paid"
  }
}
```

### Trip Details Response
```json
{
  "result": "success",
  "data": {
    "reservation_id": "reservation_123",
    "trip_details": {
      "route_info": {
        "stops": [
          {"name": "Downtown Station", "arrival": null, "departure": "15:30"},
          {"name": "Midtown Hub", "arrival": "15:45", "departure": "15:47"},
          {"name": "Airport Terminal", "arrival": "16:45", "departure": null}
        ],
        "distance": "25.3 km",
        "estimated_duration": "75 minutes"
      },
      "vehicle_info": {
        "type": "Express Bus",
        "vehicle_number": "Bus #247",
        "amenities": ["WiFi", "AC", "Wheelchair Access"]
      },
      "booking_details": {
        "passenger_count": 2,
        "seat_numbers": ["12A", "12B"],
        "special_requirements": "wheelchair_accessible"
      }
    }
  }
}
```

## ⚠️ Important Notes

### Travel Mode Support
- **Multiple Modes:** Supports bus, train, rideshare, bike, walking, and custom modes
- **Filtering:** Users can filter reservations by specific travel modes
- **Default Behavior:** Shows all travel modes when no filter specified

### Timezone Handling
- **Default Timezone:** 'America/Chicago' used when not specified
- **User Preference:** Respects user's timezone header for accurate scheduling
- **Cross-timezone Support:** Handles reservations across different time zones

### Pagination and Performance
- **Default Pagination:** 10 items per page with offset-based pagination
- **Performance Optimization:** Limits result sets to prevent large data transfers
- **Today Filter:** Special filter for showing only current day reservations

### Localization Features
- **Language Support:** Trip details can be localized based on user's locale
- **Cultural Adaptation:** Date, time, and currency formatting adapted to user's region
- **Content Translation:** Service descriptions and instructions in user's language

### Security and Privacy
- **User Scoping:** All operations scoped to authenticated user
- **Data Protection:** Personal information handled securely
- **Access Control:** Users can only access their own reservation data

## 🔗 Related File Links

- **Reservations Service:** `allrepo/connectsmart/tsp-api/src/services/reservations.js`
- **Reservations Model:** `allrepo/connectsmart/tsp-api/src/models/Reservations.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/reservations.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Static Defines:** `allrepo/connectsmart/tsp-api/src/static/defines.js`

---
*This controller provides comprehensive reservation management functionality for transportation booking and trip planning.*