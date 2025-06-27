# Uber Webhook Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates Uber webhook events and health check endpoints
- **Validation Library:** Joi
- **Related Controller:** uber-webHook.js

### 🔧 Schema Structure
```javascript
// Uber webhook event
event: {
  event_id: string (required),
  event_time: number (required),
  event_type: string (required, specific values),
  resource_href: string (required, URI format),
  meta: object (optional)
}

// Health check webhook
healthcheck: {
  event_time: number (required),
  event_type: string (required),
  data: object (required),
  resource_href: string (required, URI format)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| event_id | string | Yes | - | Unique event identifier |
| event_time | number | Yes | - | Unix timestamp |
| event_type | string | Yes | specific allowed values | Type of Uber event |
| resource_href | string | Yes | valid URI | Resource URL |
| meta.user_id | string | No | - | Uber user identifier |
| meta.org_uuid | string | No | valid UUID | Organization UUID |
| meta.resource_id | string | No | valid UUID | Resource UUID |
| meta.status | string | No | - | Event status |
| data.sender | string | Yes | - | Health check sender |
| data.message | string | Yes | - | Health check message |

### 💡 Usage Example
```javascript
// Uber trip status webhook
{
  "event_id": "12345",
  "event_time": 1640995200,
  "event_type": "guests.trips.status_changed",
  "resource_href": "https://api.uber.com/v1/trips/abc123",
  "meta": {
    "user_id": "user_456",
    "org_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "resource_id": "550e8400-e29b-41d4-a716-446655440001",
    "status": "completed"
  }
}

// Health check webhook
{
  "event_time": 1640995200,
  "event_type": "health_check",
  "data": {
    "sender": "uber_system",
    "message": "webhook_health_ok"
  },
  "resource_href": "https://api.uber.com/health"
}

// Invalid request - wrong event type
{
  "event_id": "123",
  "event_time": 1640995200,
  "event_type": "invalid_event", // Error: not in allowed values
  "resource_href": "invalid-url" // Error: must be valid URI
}
```

### ⚠️ Important Validations
- Event type restricted to specific Uber webhook events
- Resource href must be valid URI format
- Meta object UUIDs must be valid UUID format
- Event time is numeric timestamp
- Health check requires nested data object with sender and message
- Trip events include status tracking and receipt notifications

### 🏷️ Tags
**Keywords:** uber, webhook, ridehail, trip-status, health-check
**Category:** #schema #validation #joi #uber-webhook