# Incident Event Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates incident event management, notifications, and construction alerts
- **Validation Library:** Joi
- **Related Controller:** incident-events controller

## 🔧 Schema Structure
```javascript
{
  postFakeIncidentEvent: { user_id, event_id, notification_type, lat, lon, start_time, expires_time, location },
  getIncidentEvent: { user_id, min_lon, max_lon, min_lat, max_lat, version, is_affected },
  getUserInformaticEvent: { routes: [{id, polyline}], type, departure_time },
  getUnreadEvents: { user_lat, user_lon },
  postConstructionAlerts: { routes: [{id, polyline, travel_mode, times, destination_name}] }
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| user_id | number | Yes | Integer | User identifier |
| event_id | number | Yes | Integer | Event identifier |
| notification_type | number | Yes | 1-2 range | Notification type |
| lat | number | Yes | - | Event latitude |
| lon | number | Yes | - | Event longitude |
| start_time | string | Yes | - | Event start time |
| expires_time | string | Yes | - | Event expiration time |
| location | string | No | - | Event location description |
| min_lon/max_lon | number | Yes | - | Bounding box longitude |
| min_lat/max_lat | number | Yes | - | Bounding box latitude |
| routes | array | Yes | 1-5 items | Route polylines array |
| routes[].id | string | Yes | - | Route identifier |
| routes[].polyline | string/array | Yes | - | Route polyline data |
| type | number | Yes | 0-4 range | Event type |
| travel_mode | number | Yes | 0-4 range | Transportation mode |

## 💡 Usage Example
```javascript
// Create fake incident event
{
  "user_id": 123,
  "event_id": 456,
  "notification_type": 1,
  "lat": 37.7749,
  "lon": -122.4194,
  "start_time": "2024-01-15T08:00:00Z",
  "expires_time": "2024-01-15T18:00:00Z",
  "location": "Highway 101 North"
}

// Get user informatic events
{
  "routes": [
    {"id": "route_1", "polyline": "encoded_polyline_data"},
    {"id": "route_2", "polyline": "encoded_polyline_data"}
  ],
  "type": 1,
  "departure_time": 1705312800
}

// Post construction alerts
{
  "routes": [
    {
      "id": "construction_route_1",
      "polyline": ["poly1", "poly2"],
      "travel_mode": 0,
      "arrival_time": 1705316400,
      "destination_name": "Downtown Office"
    }
  ]
}
```

## ⚠️ Important Validations
- Notification type restricted to 1-2 range
- Routes array limited to 1-5 items maximum
- Event and travel mode types limited to 0-4 range
- Bounding box coordinates required for spatial queries
- Polyline can be string or array of strings
- Time fields are strings (likely ISO format)
- User and event IDs must be positive integers

## 🏷️ Tags
**Keywords:** incidents, events, notifications, construction, routes, geolocation
**Category:** #schema #validation #joi #incident-event