# Profile Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates user profile data for GET and PUT operations
- **Validation Library:** Joi
- **Related Controller:** profile controller

## 🔧 Schema Structure
```javascript
{
  get: Joi.object({ ...verifyHeaderFieldsByJoi }),
  put: Joi.object({
    ...verifyHeaderFieldsByJoi,
    security_key: Joi.string(),
    avatar: Joi.string().allow(''),
    name: { first_name, last_name },
    home: { address, latitude, longitude },
    office: { address, latitude, longitude },
    vehicle: { type, color, plate, make, pictures },
    permissions: { gps, calendar, push_notification },
    notification: { user_informatics: {...} },
    // ... additional profile fields
  })
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| avatar | string | No | Allow empty | User profile picture URL |
| name.first_name | string | No | Allow empty | User's first name |
| name.last_name | string | No | Allow empty | User's last name |
| home.address | string | No | Allow empty | Home address |
| home.latitude | number | No | Allow null | Home coordinates |
| office.address | string | No | Allow empty | Office address |
| vehicle.type | string | No | Allow empty | Vehicle type |
| permissions.gps | number | No | 0-2 range | GPS permission level |
| permissions.calendar | number | No | 0-2 range | Calendar permission level |
| gender | string | No | 'female'/'male'/'other' | User gender |
| preferred_travel_mode | string | No | Transport mode enum | Preferred transportation |
| retention_plan | number | No | 0-1 range | Retention plan status |

## 💡 Usage Example
```javascript
// Profile update request
{
  "avatar": "https://example.com/avatar.jpg",
  "name": {
    "first_name": "John",
    "last_name": "Doe"
  },
  "home": {
    "address": "123 Main St",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "permissions": {
    "gps": 2,
    "calendar": 1,
    "push_notification": 2
  },
  "gender": "male",
  "preferred_travel_mode": "driving"
}
```

## ⚠️ Important Validations
- Most fields are optional and allow empty strings
- Permission levels restricted to 0-2 range
- Gender must be one of three predefined values
- Coordinates can be null but not invalid numbers
- Security key used for frontend encryption
- Device information fields for analytics tracking

## 🏷️ Tags
**Keywords:** user profile, personal info, preferences, permissions, device tracking
**Category:** #schema #validation #joi #profile