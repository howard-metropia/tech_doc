# Weather Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates weather alert and navigation alert API endpoints
- **Validation Library:** Joi
- **Related Controller:** weather.js

### 🔧 Schema Structure
```javascript
// Route object for weather/navigation alerts
route: {
  id: string (required),
  polyline: array of strings (optional),
  travel_mode: number (required),
  destination_name: string (optional),
  arrival_time: number (optional),
  departure_time: number (optional)
}

// Weather event object
weatherEvent: {
  event_type: string (required),
  event_indicators: object (optional),
  event_location: string (optional),
  event_title: string (optional),
  event_description: string (optional),
  event_instruction: string (optional),
  event_time: string (required)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| routes | array | Yes | array of route objects | Trip routes for alerts |
| timing | string | Yes | - | Weather alert timing |
| travel_mode | number | Yes | integer | Transportation mode |
| language | string | Yes | - | Response language |
| events | array | Yes | array of event objects | Weather events |
| api_mode | string | Yes | - | API operation mode |
| current_time | string | Yes | - | Current timestamp |
| push_notification_userid | number | No | integer | User ID for notifications |

### 💡 Usage Example
```javascript
// Navigation alerts request
{
  "routes": [
    {
      "id": "route-123",
      "polyline": ["encoded_polyline_string"],
      "travel_mode": 1,
      "destination_name": "Downtown",
      "arrival_time": 1640995200,
      "departure_time": 1640991600
    }
  ]
}

// Weather test for trip
{
  "routes": [{
    "id": "route-456",
    "language": "en",
    "travel_mode": 1,
    "destination_name": "Airport",
    "departure_time": "2024-01-15T08:00:00Z",
    "events": [{
      "event_type": "severe_weather",
      "event_title": "Heavy Rain Alert",
      "event_time": "2024-01-15T09:00:00Z"
    }]
  }],
  "api_mode": "test",
  "current_time": "2024-01-15T07:30:00Z"
}

// Invalid request - missing required field
{
  "routes": [{
    "polyline": ["test"] // Error: id and travel_mode required
  }]
}
```

### ⚠️ Important Validations
- All route objects must have id and travel_mode
- Weather test endpoints require language and current_time
- Event objects need event_type and event_time at minimum
- Travel mode is integer (likely enum: 1=driving, 2=walking, etc.)
- Polyline arrays contain encoded polyline strings
- Location-based weather tests support push notifications

### 🏷️ Tags
**Keywords:** weather, alerts, navigation, routes, events, notifications
**Category:** #schema #validation #joi #weather