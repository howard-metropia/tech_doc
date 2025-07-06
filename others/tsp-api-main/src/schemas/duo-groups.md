# Duo Groups Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates duo group operations for carpooling and ride-sharing groups
- **Validation Library:** Joi  
- **Related Controller:** Duo Groups controller for group management and member operations

## 🔧 Schema Structure
```javascript
// Create group schema
{
  ...verifyHeaderFieldsByJoi,
  name: Joi.string().required(),
  types: Joi.array().items(Joi.number().integer().valid(1, 2, 3, 4, 5)).required(),
  is_private: Joi.boolean().required(),
  geofence: {
    radius: Joi.number().integer(),
    address: Joi.string(),
    latitude: Joi.number().required(),
    longitude: Joi.number().required(),
  }.required(),
  enterprise_id: Joi.number().integer().min(1),
}

// Admin profile schema
{
  ...verifyHeaderFieldsByJoi,
  group_id: Joi.number().integer().min(1).required(),
  open_contact: Joi.boolean().required(),
  gender: Joi.string().valid('female', 'male', 'other').required(),
  introduction: Joi.string().allow('').default(''),
  email: Joi.string().email().allow('').default(''),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| name | string | Yes | Any string | Group display name |
| types | array | Yes | Integers: 1,2,3,4,5 | Group type categories |
| is_private | boolean | Yes | true/false | Privacy setting |
| geofence.latitude | number | Yes | Valid number | Geographic center latitude |
| geofence.longitude | number | Yes | Valid number | Geographic center longitude |
| geofence.radius | number | No | Integer | Geofence radius in meters |
| geofence.address | string | No | Any string | Human-readable address |
| group_id | number | Yes (operations) | Min: 1 | Group identifier |
| gender | string | Yes (profile) | female/male/other | User gender |
| open_contact | boolean | Yes (profile) | true/false | Contact visibility |
| email | string | No | Valid email | Contact email address |

## 💡 Usage Example
```javascript
// Create duo group
{
  "name": "Morning Commuters",
  "types": [1, 2, 3],
  "is_private": false,
  "geofence": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "radius": 5000,
    "address": "Downtown San Francisco"
  },
  "enterprise_id": 123
}

// Create admin profile
{
  "group_id": 456,
  "open_contact": true,
  "gender": "female",
  "introduction": "Experienced commuter, happy to share rides",
  "email": "admin@example.com"
}

// Search groups
{
  "q": "commute",
  "max_lat": 37.8,
  "min_lat": 37.7,
  "max_lon": -122.3,
  "min_lon": -122.5,
  "offset": 0,
  "perpage": 10
}

// Request that fails validation
{
  "name": "Test Group",
  "types": [1, 6], // Error: 6 is not valid (must be 1-5)
  "is_private": false,
  "geofence": {
    "latitude": 37.7749
    // Error: longitude is required
  }
}
```

## ⚠️ Important Validations
- Group types must be exactly 1, 2, 3, 4, or 5 (predefined categories)
- Geofence latitude and longitude are required for location-based matching
- Gender must be one of three specific values for profile creation
- Email validation follows standard email format rules
- Group ID must be positive integer for all group operations

## 🏷️ Tags
**Keywords:** duo-groups, carpooling, geofence, group-management, ride-sharing
**Category:** #schema #validation #joi #duo-groups