# Ridehail Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates ridehail service requests, trip ordering, and status management
- **Validation Library:** Joi
- **Related Controller:** ridehail controller

## 🔧 Schema Structure
```javascript
{
  create: { pickup: {lat, lng}, dropoff: {lat, lng} },
  orderTrip: { guest: {email, phone}, locations, ridehail_trip: {product_id, fare_id} },
  getTripDetail: { trip_id: string },
  cancelTrip: { trip_id: string },
  createSbRun: { pickup, dropoff, isForcedUpdate },
  changeSbDriverStatus: { run_id: uuid, driver_state: enum }
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| pickup.latitude | number | Yes | - | Pickup location latitude |
| pickup.longitude | number | Yes | - | Pickup location longitude |
| dropoff.latitude | number | Yes | - | Dropoff location latitude |
| dropoff.longitude | number | Yes | - | Dropoff location longitude |
| guest.email | string | Yes | Valid email format | Guest user email |
| guest.phone_number | string | Yes | - | Guest phone number |
| product_id | string | Yes | UUID format | Ridehail product identifier |
| fare_id | string | Yes | UUID format | Fare estimate identifier |
| trip_id | string | Yes | - | Trip identifier for status checks |
| driver_state | string | Yes | Predefined status values | Driver status update |

## 💡 Usage Example
```javascript
// Create ridehail request
{
  "pickup": {"latitude": 37.7749, "longitude": -122.4194},
  "dropoff": {"latitude": 37.7849, "longitude": -122.4094}
}

// Order trip request
{
  "guest": {"email": "user@example.com", "phone_number": "+1234567890"},
  "pickup": {"latitude": 37.7749, "longitude": -122.4194},
  "dropoff": {"latitude": 37.7849, "longitude": -122.4094},
  "ridehail_trip": {"product_id": "uuid-here", "fare_id": "uuid-here"}
}
```

## ⚠️ Important Validations
- All coordinates must be valid numbers
- Product and fare IDs must be valid UUIDs
- Driver status must match predefined enum values
- Guest information required for trip ordering
- Benefit credit must be non-negative when provided

## 🏷️ Tags
**Keywords:** ridehail, uber, trip booking, driver status, geolocation
**Category:** #schema #validation #joi #ridehail