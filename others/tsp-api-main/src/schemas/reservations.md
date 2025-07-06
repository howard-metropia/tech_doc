# Reservations Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates reservation creation and retrieval for transportation bookings
- **Validation Library:** Joi
- **Related Controller:** reservations controller

## 🔧 Schema Structure
```javascript
{
  getAll: { userId, offset, perpage, travelMode, isToday },
  create: { zone, userId, travel_mode, origin, destination, started_on, estimated_arrival_on },
  pathParams: { id: number }
}

// Position object structure
position: {
  name: string,
  address: string,
  access_latitude: number (required),
  access_longitude: number (required),
  latitude: number (required),
  longitude: number (required)
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| userId | number | Yes | Integer | User making the reservation |
| zone | string | Yes | - | Geographic zone identifier |
| travel_mode | number | Yes | Valid enum values | Transportation mode |
| origin | object | Yes | Position object | Starting location |
| destination | object | Yes | Position object | Ending location |
| started_on | string | Yes | - | Reservation start time |
| estimated_arrival_on | string | Yes | - | Expected arrival time |
| offset | number | No | ≥ 0 | Pagination offset |
| perpage | number | No | ≥ 1 | Items per page |
| travelMode | array | No | Valid enum array | Filter by travel modes |
| isToday | boolean | No | - | Filter for today's reservations |

## 💡 Usage Example
```javascript
// Create reservation request
{
  "zone": "downtown",
  "userId": 123,
  "travel_mode": 1,
  "origin": {
    "name": "Home",
    "address": "123 Main St",
    "access_latitude": 37.7749,
    "access_longitude": -122.4194,
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "destination": {
    "name": "Office",
    "address": "456 Work Ave",
    "access_latitude": 37.7849,
    "access_longitude": -122.4094,
    "latitude": 37.7849,
    "longitude": -122.4094
  },
  "started_on": "2024-01-15T08:00:00Z",
  "estimated_arrival_on": "2024-01-15T08:30:00Z"
}
```

## ⚠️ Important Validations
- Both origin and destination require complete position objects
- Travel mode must be from predefined enum values
- Access coordinates and actual coordinates are both required
- Pagination parameters must be positive integers
- Path parameter ID must be minimum value of 1

## 🏷️ Tags
**Keywords:** reservations, bookings, travel mode, geolocation, scheduling
**Category:** #schema #validation #joi #reservations