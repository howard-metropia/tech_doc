# Trip Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates trip management operations (start, end, status, details)
- **Validation Library:** Joi
- **Related Controller:** trip.js

### 🔧 Schema Structure
```javascript
// Location object for origins and destinations
Location: {
  name: string (optional, allow empty),
  address: string (optional),
  latitude: number (required),
  longitude: number (required)
}

// Start trip request
startTrip: {
  travel_mode: number (1+, required),
  origin: Location (required),
  destination: Location (required),
  started_on: string (required),
  navigation_app: string (required, specific values),
  occupancy: number (default 1)
}

// End trip request
endTrip: {
  tripId: number (1+, required),
  destination: Location (required),
  ended_on: string (required),
  distance: number (required),
  end_type: string ('auto' or 'manual')
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| travel_mode | number/string | Yes | integer 1+ or enum values | Transportation method |
| origin/destination | object | Yes | Location schema | Trip endpoints |
| started_on/ended_on | string | Yes | - | Trip timestamps |
| navigation_app | string/number | Yes | specific values | Navigation system used |
| payment_status | number | Yes | 0, 1, or 2 | Payment processing status |
| distance | number | Yes | - | Trip distance |
| occupancy | number | No | integer, default 1 | Vehicle occupancy |
| enterprise_id | number | No | integer, min 0 | Enterprise identifier |

### 💡 Usage Example
```javascript
// Start trip request
{
  "travel_mode": 1,
  "origin": {
    "name": "Home",
    "address": "123 Main St",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "destination": {
    "name": "Work",
    "latitude": 40.7589,
    "longitude": -73.9851
  },
  "started_on": "2024-01-15T08:00:00Z",
  "navigation_app": "here",
  "occupancy": 2
}

// End trip request
{
  "tripId": 12345,
  "destination": {
    "name": "Work",
    "latitude": 40.7589,
    "longitude": -73.9851
  },
  "ended_on": "2024-01-15T08:30:00Z",
  "estimated_arrival_on": "2024-01-15T08:25:00Z",
  "distance": 5.2,
  "end_type": "manual"
}

// Invalid request - missing required field
{
  "travel_mode": 1,
  "origin": {"latitude": 40.7128} // Error: longitude required
}
```

### ⚠️ Important Validations
- Travel mode supports both numeric (1-N) and string enum values
- Navigation app accepts 'here', 'google', 'apple', 'waze' for start
- Payment status restricted to 0, 1, 2 (pending, success, failed)
- Location objects require latitude/longitude, name/address optional
- Trip details support date range filtering with ISO date format
- Enterprise filtering available for organizational trip tracking

### 🏷️ Tags
**Keywords:** trip, travel, navigation, location, payment-status
**Category:** #schema #validation #joi #trip