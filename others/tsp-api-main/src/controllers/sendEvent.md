# TSP API Send Event Controller Documentation

## 🔍 Quick Summary (TL;DR)
The sendEvent controller handles user behavior tracking and analytics event collection, allowing the platform to capture and process user interaction data for analytics and personalization.

**Keywords:** event-tracking | analytics | user-behavior | event-logging | telemetry | user-analytics | interaction-tracking | behavior-monitoring

**Primary use cases:** Tracking user interactions, collecting analytics data, monitoring feature usage, personalizing user experience

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: What types of events can be tracked?** → Any user interaction or behavior event defined by the service
- **Q: How do I send an event?** → [Send Event](#send-event-post-)
- **Q: Is authentication required?** → Yes, JWT authentication with user context
- **Q: What data is included in events?** → Event type, user ID, and event-specific metadata
- **Q: Are events processed synchronously?** → Service layer handles processing (may be async)
- **Q: How is user privacy handled?** → User ID association ensures proper data governance

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **user activity recorder** for the app. Every time you tap a button, view a screen, or complete an action, this controller records that event so the app developers can understand how people use the app, what features are popular, and how to make the experience better. It's like having a silent observer taking notes on app usage patterns.

**Technical explanation:** 
A minimal Koa.js REST controller that provides event tracking functionality for user analytics. It validates incoming event data and delegates to the event service for processing, storage, and analytics pipeline integration.

**Business value explanation:**
Essential for data-driven product development and user experience optimization. Enables understanding of user behavior patterns, feature adoption rates, and engagement metrics that drive product improvements and personalization strategies.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/sendEvent.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Analytics/Telemetry Controller
- **File Size:** ~0.7 KB
- **Complexity Score:** ⭐ (Low - Single endpoint with validation and service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/schemas/sendEvent`: Input validation schemas (**Critical**)
- `@app/src/services/sendEvent`: Event processing service (**Critical**)

## 📝 Detailed Code Analysis

### Send Event Endpoint (`POST /`)

**Purpose:** Captures and processes user interaction events for analytics

**Flow:**
1. **Authentication:** JWT authentication via auth middleware
2. **User Context:** Extracts userId from request headers
3. **Input Validation:** Validates event data against sendEvent schema
4. **Data Processing:** Converts userId to integer for consistency
5. **Service Delegation:** Passes event data to service layer for processing
6. **Response:** Returns empty success response (fire-and-forget pattern)

**Key Processing:**
```javascript
// Extract user context
const { userid: userId } = ctx.request.header;

// Validate event data
const { event } = await inputValidator.setSendEvent.validateAsync(
  ctx.request.body,
);

// Process event with user context
await service.setSendEvent({
  event,
  userId: parseInt(userId),
});
```

### Event Structure
The controller expects an event object that's validated by the schema, typically containing:
- Event type/name
- Event properties/metadata
- Timestamp (may be added by service)
- Context data

## 🚀 Usage Methods

### Track Button Click Event
```bash
curl -X POST "https://api.tsp.example.com/api/v2/send_event" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "type": "button_click",
      "properties": {
        "button_id": "book_trip",
        "screen": "home",
        "timestamp": "2024-06-25T14:30:00Z"
      }
    }
  }'
```

### Track Feature Usage
```bash
curl -X POST "https://api.tsp.example.com/api/v2/send_event" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "type": "feature_usage",
      "properties": {
        "feature_name": "route_planning",
        "action": "search_completed",
        "origin": "downtown",
        "destination": "airport",
        "modes_selected": ["bus", "walking"]
      }
    }
  }'
```

### JavaScript Client Example
```javascript
async function trackEvent(authToken, userId, eventData) {
  try {
    const response = await fetch('/api/v2/send_event', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        event: eventData
      })
    });
    
    if (response.ok) {
      console.log('Event tracked successfully');
    }
  } catch (error) {
    console.error('Event tracking failed:', error);
    // Usually fail silently to not disrupt user experience
  }
}

// Usage examples
trackEvent(authToken, userId, {
  type: 'screen_view',
  properties: {
    screen_name: 'trip_history',
    previous_screen: 'home',
    session_id: 'session_abc123'
  }
});

trackEvent(authToken, userId, {
  type: 'search_performed',
  properties: {
    search_query: 'coffee shops',
    results_count: 15,
    filters_applied: ['open_now', 'wheelchair_accessible']
  }
});
```

## 📊 Output Examples

### Successful Event Tracking
```json
{
  "result": "success",
  "data": {}
}
```

### Validation Error
```json
{
  "error": "ValidationError",
  "message": "Invalid event data",
  "details": [
    {
      "field": "event.type",
      "message": "event.type is required"
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

### Event Types
Common event categories tracked:
- **User Actions:** Button clicks, form submissions, navigation
- **Feature Usage:** Search, booking, payment, sharing
- **Screen Views:** Page/screen transitions and dwell time
- **Errors:** Client-side errors and failures
- **Performance:** Load times, API response times
- **Engagement:** Session duration, feature adoption

### Fire-and-Forget Pattern
- **Asynchronous Processing:** Events are queued for processing
- **No Blocking:** User experience not affected by analytics
- **Resilience:** Failures don't impact core functionality
- **Batching:** Service may batch events for efficiency

### Privacy and Compliance
- **User Association:** All events tied to authenticated users
- **Data Minimization:** Only necessary data collected
- **Consent Management:** Should respect user privacy preferences
- **GDPR/CCPA:** Compliance with data protection regulations

### Analytics Pipeline
- **Real-time Processing:** Some events processed immediately
- **Batch Analytics:** Others aggregated for reporting
- **Data Warehouse:** Events may flow to analytics systems
- **Machine Learning:** Event data feeds personalization models

### Performance Considerations
- **Lightweight:** Minimal processing in controller
- **Non-blocking:** Async processing in service layer
- **Rate Limiting:** May be applied to prevent abuse
- **Sampling:** High-volume events may be sampled

### Development Best Practices
- **Consistent Naming:** Use standardized event type conventions
- **Rich Properties:** Include relevant context in event properties
- **Versioning:** Consider event schema versioning
- **Documentation:** Maintain event taxonomy documentation

## 🔗 Related File Links

- **Event Service:** `allrepo/connectsmart/tsp-api/src/services/sendEvent.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/sendEvent.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This controller provides essential event tracking functionality for analytics and user behavior monitoring.*