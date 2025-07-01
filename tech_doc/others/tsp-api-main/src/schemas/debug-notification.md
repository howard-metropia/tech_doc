# Debug Notification Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates debug notification creation and updates for testing purposes
- **Validation Library:** Joi
- **Related Controller:** Debug Notification controller for testing notification systems

## 🔧 Schema Structure
```javascript
// Create debug notification schema
{
  ...verifyHeaderFieldsByJoi,
  notification_type: Joi.number().integer().min(1).required(),
  receiver_user_id: Joi.number().integer().min(1).required(),
}

// Update debug notification schema
{
  ...verifyHeaderFieldsByJoi,
  body_message: Joi.string().required(),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| notification_type | number | Yes | Integer, min: 1 | Type of notification to create |
| receiver_user_id | number | Yes | Integer, min: 1 | Target user ID for notification |
| body_message | string | Yes | Any string | Notification message content |

## 💡 Usage Example
```javascript
// Create debug notification
{
  "notification_type": 3,
  "receiver_user_id": 12345
}

// Update debug notification
{
  "body_message": "This is a test notification for debugging purposes"
}

// Request that fails validation
{
  "notification_type": 0, // Error: must be minimum 1
  "receiver_user_id": 12345
}

// Request that fails validation
{
  "notification_type": 3,
  "receiver_user_id": -1 // Error: must be minimum 1
}
```

## ⚠️ Important Validations
- Notification type must be a positive integer (minimum 1)
- Receiver user ID must be a positive integer (minimum 1)
- Body message is required for update operations
- Simple validation structure for debugging flexibility
- Header fields are included via verifyHeaderFieldsByJoi

## 🏷️ Tags
**Keywords:** debug-notification, testing, notification-system, user-targeting
**Category:** #schema #validation #joi #debug-notification