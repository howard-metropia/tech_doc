# Carpool Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates carpool creation, pricing, and management API endpoints
- **Validation Library:** Joi
- **Related Controller:** carpool.js

### 🔧 Schema Structure
```javascript
// Location object reused across schemas
location: {
  name: string (required),
  address: string (required),
  latitude: number (required),
  longitude: number (required),
  access_latitude: number (optional),
  access_longitude: number (optional)
}

// Main carpool creation schema
createCarpool: {
  role: number (1-2, required),
  origin: location (required),
  destination: location (required),
  accept_time_type: number (1-2, required),
  accept_time: array of time objects (required),
  price: number (optional, nullable),
  route_meter: number (required),
  unit_price: number (optional, nullable),
  condition: object (optional)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| role | number | Yes | integer, 1-2 | Driver (1) or passenger (2) |
| origin | object | Yes | location schema | Trip starting point |
| destination | object | Yes | location schema | Trip ending point |
| accept_time_type | number | Yes | integer, 1-2 | Time acceptance type |
| accept_time | array | Yes | objects with start_on/end_on | Available time slots |
| route_meter | number | Yes | integer | Route distance in meters |
| condition.gender | string | No | 'female', 'male', 'other' | Gender preference |
| condition.threshold_time | number | No | integer, min 0 | Time threshold |

### 💡 Usage Example
```javascript
// Valid carpool creation request
{
  "role": 1,
  "origin": {
    "name": "Downtown",
    "address": "123 Main St",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "destination": {
    "name": "Airport",
    "address": "456 Airport Rd",
    "latitude": 40.6413,
    "longitude": -73.7781
  },
  "accept_time_type": 1,
  "accept_time": [
    {"start_on": "08:00", "end_on": "09:00"}
  ],
  "route_meter": 25000
}

// Invalid request - missing required fields
{
  "role": 3, // Error: must be 1 or 2
  "origin": {"name": "test"} // Error: missing required location fields
}
```

### ⚠️ Important Validations
- Role must be exactly 1 (driver) or 2 (passenger)
- Location objects require name, address, latitude, and longitude
- Accept time array must contain valid time range objects
- Price and unit_price fields are nullable but must be numbers when provided
- Condition object allows filtering by gender and time thresholds

### 🏷️ Tags
**Keywords:** carpool, rideshare, location, pricing, time-slots
**Category:** #schema #validation #joi #carpool