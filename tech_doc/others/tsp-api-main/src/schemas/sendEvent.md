# Send Event Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates user interaction events for tracking tap/visit actions
- **Validation Library:** Joi
- **Related Controller:** sendEvent controller

## 🔧 Schema Structure
```javascript
{
  setSendEvent: Joi.object({
    event: Joi.string().valid(
      'tap_roadside',
      'tap_traffic_camera',
      'tap_transit_route',
      'tap_bikeshare_station',
      'tap_parking_garage',
      'visit_badge_page',
      'visit_help_desk'
    )
  })
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| event | string | Yes | Must be one of predefined event types | User interaction event type |

## 💡 Usage Example
```javascript
// Request example that passes validation
{
  "event": "tap_roadside"
}

// Request example that fails validation
{
  "event": "invalid_event" // Error: must be one of allowed values
}
```

## ⚠️ Important Validations
- Event type must be exactly one of the 7 predefined values
- Only tracks specific user interaction patterns
- No custom event types allowed for data consistency

## 🏷️ Tags
**Keywords:** event tracking, user interactions, analytics
**Category:** #schema #validation #joi #send-event