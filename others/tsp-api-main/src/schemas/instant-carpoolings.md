# Instant Carpoolings Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates instant carpooling session management and operations
- **Validation Library:** Joi
- **Related Controller:** instant-carpoolings controller

## 🔧 Schema Structure
```javascript
{
  create: { origin, destination, travel_time },
  getById: { id: ObjectId, userId: number },
  deleteById: { id: ObjectId, userId: number },
  joinById: { id: ObjectId, riderId: number },
  leaveById: { id: ObjectId, rider_id: number },
  startById: { id: ObjectId, estimated_arrival_on, navigation_app },
  finishById: { id: ObjectId, userId, distance, destination, end_type, navigation_app },
  commentById: { id: ObjectId, userId, rating, feedback },
  getHistory: { userId, offset, perpage }
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| id | string | Yes | 24-char hex ObjectId | MongoDB document ID |
| origin | object | Yes | Position object (lat/lng/address) | Starting location |
| destination | object | Yes | Position object (lat/lng/address) | Ending location |
| travel_time | number | Yes | Integer ≥ 0 | Expected travel duration |
| userId | number | Yes | Integer ≥ 1 | User performing action |
| riderId | number | Yes | Integer ≥ 1 | Passenger joining carpool |
| estimated_arrival_on | number | Yes | Integer ≥ 0 | Expected arrival timestamp |
| navigation_app | string | No | 'here'/'google'/'apple'/'waze' | Navigation app choice |
| distance | number | Yes | Integer ≥ 0 | Trip distance in meters |
| rating | number | Yes | 0-5 range | Trip rating score |
| feedback | string | No | Allow empty, default '' | Trip feedback text |
| end_type | string | No | 'auto'/'manual' | Trip completion method |

## 💡 Usage Example
```javascript
// Create instant carpool
{
  "origin": {
    "name": "Home",
    "address": "123 Main St",
    "access_latitude": 37.7749,
    "access_longitude": -122.4194,
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "destination": {
    "latitude": 37.7849,
    "longitude": -122.4094
  },
  "travel_time": 1800
}

// Join carpool session
{
  "id": "507f1f77bcf86cd799439011",
  "riderId": 456
}

// Rate completed trip
{
  "id": "507f1f77bcf86cd799439011",
  "userId": 123,
  "rating": 4.5,
  "feedback": "Great ride!"
}
```

## ⚠️ Important Validations
- MongoDB ObjectId must be exactly 24 hexadecimal characters
- Position objects require access and actual coordinates
- User and rider IDs must be positive integers
- Rating must be within 0-5 range
- Navigation apps limited to four supported options
- Travel time and distance must be non-negative integers

## 🏷️ Tags
**Keywords:** carpooling, instant rides, mongodb, rating, navigation, geolocation
**Category:** #schema #validation #joi #instant-carpoolings