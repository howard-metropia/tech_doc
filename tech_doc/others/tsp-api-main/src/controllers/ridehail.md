# TSP API Ridehail Controller Documentation

## 🔍 Quick Summary (TL;DR)
The ridehail controller integrates with ridesharing services like Uber to provide ride estimation, booking, tracking, and management functionality within the TSP platform's multimodal transportation ecosystem.

**Keywords:** ridehail | uber-integration | ride-booking | eta-estimation | pickup-points | trip-management | rideshare | on-demand-transport | sandbox-testing

**Primary use cases:** Getting ride estimates, finding pickup points, booking rideshare trips, tracking ride status, canceling rides

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, Uber API integration, sandbox testing support

## ❓ Common Questions Quick Index
- **Q: How do I get ride time estimates?** → [Get Uber ETA](#get-uber-eta-post-uber_estimation)
- **Q: How do I find optimal pickup locations?** → [Get Pickup Points](#get-pickup-points-get-pickup_point)
- **Q: How do I book a rideshare trip?** → [Order Trip](#order-trip-post-ridehail)
- **Q: How do I check my ride status?** → [Get Trip Details](#get-trip-details-get-ridehailtrip_id)
- **Q: How do I cancel a booked ride?** → [Cancel Trip](#cancel-trip-delete-ridehailtrip_id)
- **Q: Are there testing features?** → Yes, sandbox endpoints for non-production environments

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **rideshare booking assistant** within the transportation app. Instead of switching between different ride apps, this controller lets you get ride estimates, find the best pickup spots, book rides, track your driver, and cancel if needed - all from within the main transportation platform. It's like having Uber built right into your trip planning app.

**Technical explanation:** 
A comprehensive Koa.js REST controller that provides full ridehail service integration, primarily with Uber's API. It handles ride estimation, pickup point optimization, trip booking and management, with additional sandbox functionality for testing in non-production environments.

**Business value explanation:**
Essential for providing complete multimodal transportation solutions. Enables seamless integration of on-demand rideshare services with public transit, walking, and cycling options, creating a unified mobility platform that increases user convenience and platform stickiness.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/ridehail.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Third-party Integration Controller
- **File Size:** ~2.4 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - External API integration, trip management, real-time data)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/helpers/fields-of-header`: Header field extraction utility (**High**)
- `@app/src/schemas/ridehail`: Input validation schemas (**Critical**)
- `@app/src/services/ridehail`: Ridehail business logic service (**Critical**)

## 📝 Detailed Code Analysis

### Production Endpoints

#### Get Uber ETA (`POST /uber_estimation`)
- **Purpose:** Retrieves estimated arrival times and pricing for ridehail services
- **Input Processing:** Combines header context with request body for location data
- **Service Call:** `service.create(input)` for external API integration

#### Get Pickup Points (`GET /pickup_point`)
- **Purpose:** Finds optimal pickup locations based on current location
- **Input Sources:** Headers + query parameters for location and preferences
- **Optimization:** Service layer handles pickup point optimization algorithms

#### Order Trip (`POST /ridehail`)
- **Purpose:** Books ridehail trips through integrated services
- **Service Call:** `service.orderGuestTrip(input)` for trip booking
- **Payment Integration:** Handles payment processing through service layer

#### Get Trip Details (`GET /ridehail/:trip_id`)
- **Purpose:** Retrieves real-time trip information and driver details
- **Security:** User-scoped access to trip information
- **Real-time Data:** Live tracking and status updates

#### Cancel Trip (`DELETE /ridehail/:trip_id`)
- **Purpose:** Cancels booked ridehail trips with appropriate handling
- **Validation:** Ensures user can only cancel their own trips
- **Business Logic:** Handles cancellation policies and potential fees

### Development/Testing Endpoints (Non-Production Only)

#### Create Sandbox Run (`POST /sandbox/run`)
- **Environment Check:** Only available when `PROJECT_STAGE !== 'production'`
- **Purpose:** Simulates ride scenarios for testing
- **Testing Support:** Enables comprehensive integration testing

#### Change Sandbox Driver Status (`POST /sandbox/driver_status`)
- **Purpose:** Simulates driver status changes for testing scenarios
- **Development Tool:** Helps test various ride states and transitions

## 🚀 Usage Methods

### Get Ride Estimates
```bash
curl -X POST "https://api.tsp.example.com/api/v2/uber_estimation" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_latitude": 29.7604,
    "pickup_longitude": -95.3698,
    "dropoff_latitude": 29.7749,
    "dropoff_longitude": -95.3628,
    "ride_type": "uberX"
  }'
```

### Find Pickup Points
```bash
curl -X GET "https://api.tsp.example.com/api/v2/pickup_point?latitude=29.7604&longitude=-95.3698&radius=500" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Book a Ride
```bash
curl -X POST "https://api.tsp.example.com/api/v2/ridehail" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_latitude": 29.7604,
    "pickup_longitude": -95.3698,
    "dropoff_latitude": 29.7749,
    "dropoff_longitude": -95.3628,
    "ride_type": "uberX",
    "passenger_count": 2,
    "payment_method_id": "pm_12345",
    "notes": "Blue building, main entrance"
  }'
```

### Check Trip Status
```bash
curl -X GET "https://api.tsp.example.com/api/v2/ridehail/trip_abc123" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Cancel Trip
```bash
curl -X DELETE "https://api.tsp.example.com/api/v2/ridehail/trip_abc123" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

## 📊 Output Examples

### Ride Estimation Response
```json
{
  "result": "success",
  "data": {
    "estimates": [
      {
        "product_id": "uberX",
        "display_name": "UberX",
        "eta_minutes": 8,
        "price_estimate": {
          "low": 12.50,
          "high": 16.75,
          "currency": "USD"
        },
        "distance": 5.2,
        "duration": 18
      }
    ],
    "pickup_location": {
      "latitude": 29.7604,
      "longitude": -95.3698,
      "address": "Downtown Houston"
    }
  }
}
```

### Trip Booking Response
```json
{
  "result": "success",
  "data": {
    "trip_id": "trip_abc123",
    "status": "processing",
    "estimated_pickup_time": "2024-06-25T15:38:00Z",
    "driver_info": null,
    "fare": {
      "estimated_total": 14.25,
      "currency": "USD"
    },
    "tracking_url": "https://uber.com/track/trip_abc123"
  }
}
```

### Trip Details Response
```json
{
  "result": "success",
  "data": {
    "trip_id": "trip_abc123",
    "status": "arriving",
    "driver": {
      "name": "John Driver",
      "phone": "+1-555-0123",
      "vehicle": {
        "make": "Toyota",
        "model": "Camry",
        "license_plate": "ABC-1234",
        "color": "Blue"
      },
      "location": {
        "latitude": 29.7590,
        "longitude": -95.3685,
        "bearing": 45
      }
    },
    "eta_minutes": 3,
    "fare": {
      "total": 14.25,
      "currency": "USD"
    }
  }
}
```

### Pickup Points Response
```json
{
  "result": "success",
  "data": {
    "pickup_points": [
      {
        "latitude": 29.7604,
        "longitude": -95.3698,
        "address": "Main St & Bell St",
        "walk_time_seconds": 120,
        "pickup_type": "street_corner"
      },
      {
        "latitude": 29.7610,
        "longitude": -95.3705,
        "address": "Downtown Transit Center",
        "walk_time_seconds": 180,
        "pickup_type": "transit_hub"
      }
    ]
  }
}
```

## ⚠️ Important Notes

### External API Integration
- **Uber Partnership:** Primary integration with Uber's API services
- **Real-time Data:** Live tracking and status updates from ridehail providers
- **API Dependencies:** Service availability depends on external provider status
- **Rate Limiting:** Uber API rate limits may affect high-volume usage

### Environment-Specific Features
- **Production Safety:** Sandbox endpoints disabled in production environments
- **Testing Support:** Comprehensive testing tools for development and QA
- **Configuration Management:** Environment-specific API keys and endpoints

### Payment Integration
- **Secure Processing:** Payment methods handled through secure service layer
- **Multiple Options:** Support for various payment methods (credit cards, digital wallets)
- **Fare Calculation:** Real-time fare estimates and final billing

### Trip Management Features
- **Lifecycle Tracking:** Complete trip lifecycle from booking to completion
- **Real-time Updates:** Live driver location and ETA updates
- **Cancellation Policies:** Provider-specific cancellation rules and fees
- **History Tracking:** Complete trip history and receipt management

### Business Logic Considerations
- **Multimodal Integration:** Seamless integration with other transportation modes
- **Optimization Algorithms:** Pickup point optimization for user convenience
- **Service Selection:** Automatic selection of best available ride options
- **Fallback Mechanisms:** Handling of service unavailability scenarios

## 🔗 Related File Links

- **Ridehail Service:** `allrepo/connectsmart/tsp-api/src/services/ridehail.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/ridehail.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Header Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

---
*This controller provides comprehensive ridehail integration for seamless on-demand transportation within the multimodal TSP platform.*