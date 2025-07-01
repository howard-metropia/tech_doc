# TSP API User Actions Controller Documentation

## 🔍 Quick Summary (TL;DR)
The user actions controller records user behavior and interaction events for analytics, safety monitoring, and feature usage tracking within the transportation platform.

**Keywords:** user-actions | behavior-tracking | analytics | safety-events | school-zones | pre-trip-alerts | user-analytics | interaction-logging

**Primary use cases:** Recording user interactions, tracking safety events, monitoring school zone entries, logging pre-trip alerts, collecting behavioral analytics

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, MongoDB for user actions storage

## ❓ Common Questions Quick Index
- **Q: What user actions are tracked?** → Safety events, school zone entries, pre-trip alerts, and custom interactions
- **Q: Are debug users tracked?** → No, debug users' actions are ignored
- **Q: How is location data handled?** → Enriched with region information for school zone events
- **Q: What happens with timestamps?** → Pre-trip alert event times are parsed and stored as Date objects
- **Q: Is authentication required?** → Yes, JWT authentication with user context
- **Q: How are actions stored?** → In MongoDB with action type and custom attributes

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital behavior recorder** for the transportation app. It keeps track of important things users do - like when they get safety alerts before trips, when they drive through school zones, or how they interact with different features. This helps improve the app and keep people safe by understanding how they actually use the transportation system.

**Technical explanation:** 
A Koa.js REST controller that processes and stores user behavior events with contextual enrichment. It validates action data, filters out debug users, enriches location-based events with regional information, and stores timestamped actions in MongoDB for analytics and safety monitoring.

**Business value explanation:**
Critical for user experience optimization, safety compliance, and data-driven product development. Enables understanding of user behavior patterns, safety event monitoring, compliance with school zone regulations, and evidence-based feature improvements through comprehensive interaction tracking.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/user-actions.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** User Analytics Controller
- **File Size:** ~1.5 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Data enrichment and conditional processing)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@app/src/schemas/user-actions`: Input validation schemas (**Critical**)
- `@app/src/models/UserActions`: MongoDB model for actions (**Critical**)
- `@app/src/models/AuthUsers`: User data model (**Critical**)
- `@app/src/helpers/get-region-code`: Location enrichment (**High**)

## 📝 Detailed Code Analysis

### Add User Actions Endpoint (`POST /user_actions`)

**Purpose:** Records multiple user actions with contextual data enrichment

**Processing Flow:**
1. **Authentication:** JWT validation and user context extraction
2. **Input Validation:** Validates actions array and user data
3. **User Verification:** Checks if user is debug user (skips tracking)
4. **Action Processing:** Processes each action with specific enrichment
5. **Data Storage:** Creates MongoDB records for each action
6. **Response:** Returns array of created action IDs

**Debug User Filtering:**
```javascript
const userData = await AuthUsers.query().findById(userId);
if (!userData.is_debug) {
  // Process actions only for non-debug users
}
```

**Special Action Processing:**

**Pre-trip Alert Events:**
```javascript
if (action === userActionList.preTripAlertOpen && attributes) {
  attributes.event_time = new Date(attributes.event_time);
}
```

**School Zone Events:**
```javascript
if (action === userActionList.enterSchoolZone || 
    action === userActionList.enterSchoolZoneSpeeding) {
  const { latitude, longitude } = attributes;
  attributes.region_info = await getRegionCode({
    lat: latitude,
    lon: longitude,
  });
}
```

**Action Storage:**
```javascript
const result = await UserActions.create({
  userId,
  action,
  attributes,
});
return result._id;
```

## 🚀 Usage Methods

### Record Single Action
```bash
curl -X POST "https://api.tsp.example.com/api/v2/user_actions" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      {
        "action": "pre_trip_alert_open",
        "attributes": {
          "event_time": "2024-06-25T08:30:00Z",
          "alert_type": "speed_limit_change",
          "route_id": "route_123"
        }
      }
    ]
  }'
```

### Record Multiple Actions
```bash
curl -X POST "https://api.tsp.example.com/api/v2/user_actions" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      {
        "action": "enter_school_zone",
        "attributes": {
          "latitude": 37.7749,
          "longitude": -122.4194,
          "speed_mph": 15,
          "speed_limit": 25,
          "timestamp": "2024-06-25T14:30:00Z"
        }
      },
      {
        "action": "feature_interaction",
        "attributes": {
          "feature_name": "trip_planning",
          "interaction_type": "button_click",
          "screen": "home"
        }
      }
    ]
  }'
```

### Record School Zone Speeding Event
```bash
curl -X POST "https://api.tsp.example.com/api/v2/user_actions" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      {
        "action": "enter_school_zone_speeding",
        "attributes": {
          "latitude": 37.7849,
          "longitude": -122.4094,
          "speed_mph": 35,
          "speed_limit": 25,
          "excess_speed": 10,
          "school_name": "Lincoln Elementary",
          "timestamp": "2024-06-25T15:45:00Z"
        }
      }
    ]
  }'
```

### JavaScript Client Example
```javascript
async function recordUserActions(authToken, userId, actions) {
  try {
    const response = await fetch('/api/v2/user_actions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        actions: actions
      })
    });
    
    const result = await response.json();
    
    if (result.result === 'success') {
      console.log('Actions recorded:', result.data.ids);
      return result.data.ids;
    } else {
      console.error('Failed to record actions:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('User actions recording error:', error);
    throw error;
  }
}

// Usage examples
recordUserActions(token, 'usr_12345', [
  {
    action: 'pre_trip_alert_open',
    attributes: {
      event_time: new Date().toISOString(),
      alert_type: 'traffic_alert',
      severity: 'medium'
    }
  }
]);

recordUserActions(token, 'usr_12345', [
  {
    action: 'enter_school_zone',
    attributes: {
      latitude: 37.7749,
      longitude: -122.4194,
      speed_mph: 20,
      speed_limit: 25
    }
  },
  {
    action: 'feature_usage',
    attributes: {
      feature: 'voice_navigation',
      duration_seconds: 120
    }
  }
]);
```

## 📊 Output Examples

### Successful Action Recording
```json
{
  "result": "success",
  "data": {
    "ids": [
      "60a7c8b4f1d2e3f4a5b6c7d8",
      "60a7c8b5f1d2e3f4a5b6c7d9"
    ]
  }
}
```

### Debug User Response (No Actions Recorded)
```json
{
  "result": "success",
  "data": {
    "ids": []
  }
}
```

### Validation Error
```json
{
  "error": "ValidationError",
  "message": "Invalid action data",
  "details": [
    {
      "field": "actions[0].action",
      "message": "action is required"
    },
    {
      "field": "actions[1].attributes.latitude",
      "message": "latitude must be between -90 and 90"
    }
  ]
}
```

### Authentication Error
```json
{
  "error": "AuthenticationError",
  "message": "Invalid or expired JWT token",
  "code": 401
}
```

## ⚠️ Important Notes

### Action Types
Common user action categories:
- **Safety Events:** Pre-trip alerts, speed warnings, hazard notifications
- **School Zone Events:** Zone entry, speeding violations, time-based restrictions
- **Navigation Events:** Route selection, turn-by-turn interactions, rerouting
- **Feature Usage:** Screen views, button clicks, setting changes
- **Trip Events:** Trip start/end, mode changes, interruptions
- **Social Events:** Sharing, rating, feedback submission

### Data Enrichment

**School Zone Enhancement:**
- Automatic region code lookup for school zone events
- Geographic context for compliance and analytics
- Location-based safety monitoring

**Timestamp Processing:**
- Pre-trip alert times converted to Date objects
- Timezone-aware timestamp handling
- Event sequence tracking

### Debug User Handling
- **Exclusion Logic:** Debug users' actions are not recorded
- **Development Testing:** Allows testing without polluting analytics
- **Data Quality:** Ensures production analytics accuracy
- **Performance:** Reduces unnecessary data processing

### MongoDB Storage
- **Flexible Schema:** Actions can have varying attributes
- **Scalability:** MongoDB handles high-volume action logging
- **Indexing:** Requires proper indexing for query performance
- **Analytics:** Enables complex analytics queries

### Privacy and Compliance
- **User Consent:** Should align with privacy policy
- **Data Retention:** Implement appropriate retention policies
- **Anonymization:** Consider anonymizing sensitive location data
- **GDPR/CCPA:** Ensure compliance with data protection regulations

### Performance Considerations
- **Batch Processing:** Multiple actions processed in single request
- **Async Operations:** Database writes don't block response
- **Error Handling:** Individual action failures don't affect others
- **Rate Limiting:** May implement limits to prevent abuse

### Analytics Applications
- **User Behavior Analysis:** Understanding interaction patterns
- **Safety Monitoring:** Tracking compliance and violations
- **Feature Adoption:** Measuring feature usage and effectiveness
- **Performance Metrics:** User engagement and retention analysis

### Error Scenarios
- **Network Failures:** Actions may be queued for retry
- **Validation Errors:** Invalid action data rejected
- **Database Errors:** Storage failures logged and handled
- **Authentication Issues:** Unauthorized requests blocked

## 🔗 Related File Links

- **User Actions Model:** `allrepo/connectsmart/tsp-api/src/models/UserActions.js`
- **Auth Users Model:** `allrepo/connectsmart/tsp-api/src/models/AuthUsers.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/user-actions.js`
- **Action Definitions:** `allrepo/connectsmart/tsp-api/src/static/defines.js`
- **Region Helper:** `allrepo/connectsmart/tsp-api/src/helpers/get-region-code.js`
- **Header Helper:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

---
*This controller provides comprehensive user behavior tracking essential for analytics, safety monitoring, and product optimization.*