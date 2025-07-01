# Trace Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates user location tracking and visit logging
- **Validation Library:** Joi
- **Related Controller:** trace.js

### 🔧 Schema Structure
```javascript
// Custom precision function for coordinates
customPrecision: (value) => Math.floor(value * 1000000) / 1000000

// User visit tracking
userVisit: {
  userid: number (required),
  latitude: number (required, custom precision),
  longitude: number (required, custom precision),
  arrival_date: date (required, timestamp),
  departure_date: date (required, timestamp),
  os_type: string (optional)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| userid | number | Yes | - | User identifier |
| latitude | number | Yes | 6 decimal precision | Location latitude |
| longitude | number | Yes | 6 decimal precision | Location longitude |
| arrival_date | date | Yes | timestamp format | Visit start time |
| departure_date | date | Yes | timestamp format | Visit end time |
| os_type | string | No | - | Operating system type |

### 💡 Usage Example
```javascript
// User visit tracking
{
  "userid": 12345,
  "latitude": 40.712800,
  "longitude": -74.006000,
  "arrival_date": 1640995200000,
  "departure_date": 1640998800000,
  "os_type": "iOS"
}

// Coordinate precision handling
{
  "userid": 67890,
  "latitude": 40.7128123456789, // Truncated to 40.712812
  "longitude": -74.0060987654321, // Truncated to -74.006098
  "arrival_date": 1640995200000,
  "departure_date": 1640998800000
}

// Invalid request - missing required field
{
  "userid": 12345,
  "latitude": 40.712800
  // Error: longitude required
}
```

### ⚠️ Important Validations
- Coordinates limited to 6 decimal places precision (±1 meter accuracy)
- Custom precision function truncates rather than rounds coordinates
- Arrival and departure dates must be timestamp format
- User ID is required numeric identifier
- OS type is optional for device tracking
- Timestamps likely in milliseconds since epoch

### 🏷️ Tags
**Keywords:** tracking, location, coordinates, visits, precision
**Category:** #schema #validation #joi #trace