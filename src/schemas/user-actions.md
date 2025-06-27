# User Actions Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates user action tracking and analytics events
- **Validation Library:** Joi
- **Related Controller:** user-actions.js

### 🔧 Schema Structure
```javascript
// User action creation
create: {
  actions: array of action objects (required, min 1)
}

// Action object structure
action: {
  action: string (required),
  attributes: object (optional)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| actions | array | Yes | min 1 item | Array of user action events |
| action | string | Yes | - | Action type/name identifier |
| attributes | object | No | - | Additional action metadata |

### 💡 Usage Example
```javascript
// Track multiple user actions
{
  "actions": [
    {
      "action": "button_click",
      "attributes": {
        "button_id": "search_button",
        "screen": "home",
        "timestamp": 1640995200
      }
    },
    {
      "action": "page_view",
      "attributes": {
        "page": "trip_details",
        "duration": 45
      }
    }
  ]
}

// Simple action without attributes
{
  "actions": [
    {
      "action": "app_open"
    }
  ]
}

// Invalid request - empty actions array
{
  "actions": [] // Error: must contain at least 1 item
}

// Invalid request - missing action field
{
  "actions": [
    {
      "attributes": {"test": "value"} // Error: action field required
    }
  ]
}
```

### ⚠️ Important Validations
- Actions array must contain at least one action object
- Each action object requires an action string identifier
- Attributes object is completely optional and flexible
- All requests require header verification fields
- Supports batch processing of multiple actions
- No restrictions on attributes object structure

### 🏷️ Tags
**Keywords:** analytics, tracking, user-behavior, events
**Category:** #schema #validation #joi #user-actions