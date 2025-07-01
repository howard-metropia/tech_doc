# TSP API User Preference Controller Documentation

## 🔍 Quick Summary (TL;DR)
The preference controller manages user-specific application settings and preferences, providing endpoints to retrieve, update, and reset user customization options for the TSP platform.

**Keywords:** user-preferences | settings | customization | user-configuration | defaults | personalization | application-settings | user-profile

**Primary use cases:** Managing user app preferences, updating notification settings, retrieving default configurations, personalizing user experience

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I get my current preferences?** → [Get User Preferences](#get-user-preferences-get-preference)
- **Q: How do I update my settings?** → [Update Preferences](#update-preferences-put-preference)
- **Q: How do I reset to default settings?** → [Get Default Preferences](#get-default-preferences-get-preference_default)
- **Q: What preferences can be customized?** → Notification settings, theme options, language, transport modes
- **Q: Are preferences synced across devices?** → Yes, tied to user account for cross-device consistency
- **Q: What authentication is required?** → JWT authentication with user context headers

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **personal settings manager** for the transportation app. Just like how you can customize your phone's settings for notifications, themes, and apps, this controller lets you save and manage your preferences for how you want the transportation app to work - like your favorite transport modes, notification preferences, language settings, and other personal choices.

**Technical explanation:** 
A standard Koa.js REST controller providing CRUD operations for user preference management. It handles preference retrieval, updates, and default configuration access with comprehensive input validation and user context extraction from headers.

**Business value explanation:**
Essential for user experience personalization and retention. Customizable preferences increase user satisfaction, engagement, and platform stickiness by allowing users to tailor the application to their specific needs and usage patterns.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/preference.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** User Settings/Configuration Controller
- **File Size:** ~1.3 KB
- **Complexity Score:** ⭐⭐ (Medium - CRUD operations with validation and header processing)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/helpers/fields-of-header`: Header field extraction utility (**High**)
- `@app/src/schemas/preference`: Input validation schemas (**Critical**)
- `@app/src/services/preference`: Preference business logic service (**Critical**)

## 📝 Detailed Code Analysis

### Available Endpoints

#### Get User Preferences (`GET /preference`)
- **Purpose:** Retrieves current user preferences and settings
- **Input Sources:** Headers (user context) + query parameters
- **Validation:** Uses `inputValidator.get` schema
- **Service Call:** `services.get(input)` with validated data

#### Update Preferences (`PUT /preference`)
- **Purpose:** Updates user preferences with new settings
- **Input Sources:** Headers (user context) + request body
- **Validation:** Uses `inputValidator.update` schema  
- **Service Call:** `services.update(input)` with validated data

#### Get Default Preferences (`GET /preference_default`)
- **Purpose:** Retrieves system default preference settings
- **Input Sources:** Headers (user context) + query parameters
- **Validation:** Uses `inputValidator.getDefault` schema
- **Service Call:** `services.getDefault(input)` for defaults

### Input Processing Pattern
All endpoints follow a consistent pattern:
```javascript
const input = await inputValidator.{operation}.validateAsync({
  ...fetchFieldsFromHeader(ctx.request.header),
  ...ctx.request.{body|query},
});
```

This pattern ensures:
- User context extraction from headers
- Input validation with appropriate schemas
- Clean data passed to service layer

## 🚀 Usage Methods

### Get Current Preferences
```bash
curl -X GET "https://api.tsp.example.com/api/v1/preference" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Update User Preferences
```bash
curl -X PUT "https://api.tsp.example.com/api/v1/preference" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "notifications": {
      "push_enabled": true,
      "email_enabled": false,
      "trip_alerts": true,
      "promotional": false
    },
    "transport_preferences": {
      "preferred_modes": ["bus", "walking", "cycling"],
      "max_walking_distance": 800,
      "accessibility_needed": false
    },
    "app_settings": {
      "language": "en-US",
      "theme": "light",
      "units": "metric"
    }
  }'
```

### Get Default Settings
```bash
curl -X GET "https://api.tsp.example.com/api/v1/preference_default" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### JavaScript Client Example
```javascript
async function getUserPreferences(authToken, userId) {
  try {
    const response = await fetch('/api/v1/preference', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.data;
    }
  } catch (error) {
    console.error('Failed to fetch preferences:', error);
  }
}

async function updatePreferences(authToken, userId, preferences) {
  try {
    const response = await fetch('/api/v1/preference', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(preferences)
    });
    
    if (response.ok) {
      const result = await response.json();
      return result.data;
    }
  } catch (error) {
    console.error('Failed to update preferences:', error);
  }
}
```

## 📊 Output Examples

### User Preferences Response
```json
{
  "result": "success",
  "data": {
    "user_id": "usr_12345",
    "notifications": {
      "push_enabled": true,
      "email_enabled": false,
      "trip_alerts": true,
      "promotional": false,
      "quiet_hours": {
        "enabled": true,
        "start": "22:00",
        "end": "08:00"
      }
    },
    "transport_preferences": {
      "preferred_modes": ["bus", "walking", "cycling"],
      "max_walking_distance": 800,
      "max_cycling_distance": 5000,
      "accessibility_needed": false,
      "avoid_tolls": true
    },
    "app_settings": {
      "language": "en-US",
      "theme": "light",
      "units": "metric",
      "map_style": "default"
    },
    "privacy": {
      "location_sharing": true,
      "analytics": true,
      "marketing": false
    },
    "updated_at": "2024-06-25T14:30:00Z"
  }
}
```

### Default Preferences Response
```json
{
  "result": "success",
  "data": {
    "default_preferences": {
      "notifications": {
        "push_enabled": true,
        "email_enabled": true,
        "trip_alerts": true,
        "promotional": true
      },
      "transport_preferences": {
        "preferred_modes": ["walking", "bus"],
        "max_walking_distance": 1000,
        "accessibility_needed": false
      },
      "app_settings": {
        "language": "en-US",
        "theme": "light",
        "units": "imperial"
      }
    }
  }
}
```

### Update Success Response
```json
{
  "result": "success",
  "data": {
    "updated": true,
    "updated_at": "2024-06-25T14:30:00Z",
    "preferences": {
      "notifications": {
        "push_enabled": false,
        "email_enabled": true
      }
    }
  }
}
```

## ⚠️ Important Notes

### Preference Categories
- **Notifications:** Push notifications, email preferences, alert settings
- **Transport:** Preferred modes, distance limits, accessibility needs
- **App Settings:** Language, theme, units, display preferences
- **Privacy:** Data sharing, analytics, marketing preferences

### Data Persistence
- **User-Scoped:** All preferences tied to authenticated user account
- **Cross-Device Sync:** Preferences synced across user's devices
- **Version Control:** Preference updates include timestamps for tracking
- **Backup/Restore:** Integration with user profile backup systems

### Validation and Security
- **Input Validation:** Comprehensive validation for all preference updates
- **Authentication Required:** All operations require valid user authentication
- **Data Integrity:** Prevents invalid preference configurations
- **Rate Limiting:** May include rate limiting to prevent abuse

### Business Logic Integration
- **Default Management:** System-wide default preferences for new users
- **Feature Flags:** Preferences may control feature availability
- **A/B Testing:** Preference system may integrate with testing frameworks
- **Analytics:** Preference changes tracked for user experience insights

### Migration and Compatibility
- **Schema Evolution:** Preference schema can evolve with new features
- **Backward Compatibility:** Older app versions gracefully handle new preferences
- **Migration Scripts:** Automatic migration for preference schema changes
- **Validation Rules:** Ensures preference values remain valid over time

## 🔗 Related File Links

- **Preference Service:** `allrepo/connectsmart/tsp-api/src/services/preference.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/preference.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Header Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

---
*This controller provides essential user preference management for application personalization and user experience optimization.*