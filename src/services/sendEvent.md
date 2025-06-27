# TSP API SendEvent Service Documentation

## 🔍 Quick Summary (TL;DR)
The SendEvent service maps user interaction events from the mobile app to standardized event categories and dispatches them to the event tracking system for analytics, user behavior monitoring, and feature usage analysis.

**Keywords:** event-tracking | user-analytics | interaction-mapping | traveler-info | visit-events | app-engagement | behavior-monitoring

**Primary use cases:** Tracking user interactions with map elements, monitoring page visits, analyzing app engagement patterns, collecting usage analytics

**Compatibility:** Node.js >= 16.0.0, event helper integration, simple mapping logic for mobile app interactions

## ❓ Common Questions Quick Index
- **Q: What events are tracked?** → Map interactions (roadside, cameras, transit) and page visits (badges, help)
- **Q: How are events categorized?** → Two main categories: traveler_info and visit_event
- **Q: What data is sent?** → User ID, event name, and action metadata
- **Q: How is the event system triggered?** → Mobile app calls trigger event mapping and dispatch
- **Q: What happens to unmapped events?** → They are ignored and not sent to the tracking system
- **Q: Is event data logged?** → Yes, successful event dispatches are logged with user and action details

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **interaction tracker** that watches what users tap or visit in the mobile app and translates those actions into organized categories for analysis. When someone taps on a traffic camera or visits the help page, this service records it for understanding user behavior.

**Technical explanation:** 
A lightweight event mapping and dispatch service that categorizes mobile app user interactions into standardized event types and forwards them to the event tracking system. Provides simple mapping logic from specific user actions to broader analytical categories.

**Business value explanation:**
Enables user behavior analytics, supports feature usage tracking, provides insights for app improvement decisions, helps understand user engagement patterns, and supports data-driven product development.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/sendEvent.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with event helper integration
- **Type:** Event Mapping and Dispatch Service
- **File Size:** ~1.1 KB
- **Complexity Score:** ⭐ (Low - Simple mapping logic)

**Dependencies:**
- `@maas/core/log`: Logging infrastructure (**Medium**)
- `@app/src/helpers/send-event`: Event dispatch helper (**Critical**)

## 📝 Detailed Code Analysis

### setSendEvent Function

**Purpose:** Maps user interactions to event categories and dispatches to tracking system

**Parameters:**
- `eventData.event`: String - Specific user action identifier
- `eventData.userId`: Number - User performing the action

**Returns:** Promise (void)

### Event Mapping Logic

```javascript
const setSendEvent = async (eventData) => {
  const { event, userId } = eventData;

  const eventParams = {
    userIds: [userId],
    eventName: '',
    eventMeta: { action: event },
  };

  switch (event) {
    case 'tap_roadside':
    case 'tap_traffic_camera':
    case 'tap_transit_route':
    case 'tap_bikeshare_station':
    case 'tap_parking_garage': {
      eventParams.eventName = 'traveler_info';
      break;
    }
    case 'visit_badge_page':
    case 'visit_help_desk': {
      eventParams.eventName = 'visit_event';
      break;
    }
  }

  if (eventParams.eventName !== '') {
    await sendEvent([eventParams]);
    logger.info(`[send-event] user ${userId} make event "${event}" to send`);
  }
};
```

### Event Categories

#### Traveler Info Events
- **tap_roadside**: User taps on roadside assistance information
- **tap_traffic_camera**: User views traffic camera feeds
- **tap_transit_route**: User interacts with transit route information
- **tap_bikeshare_station**: User checks bike share station details
- **tap_parking_garage**: User views parking garage information

#### Visit Events
- **visit_badge_page**: User navigates to achievement/badge section
- **visit_help_desk**: User accesses help or support features

### Event Processing Flow

1. **Input Validation**: Extracts event type and user ID from request data
2. **Event Mapping**: Uses switch statement to categorize specific actions
3. **Conditional Dispatch**: Only sends events with valid mappings
4. **Logging**: Records successful event dispatches for monitoring

## 🚀 Usage Methods

### Basic Event Tracking
```javascript
const sendEventService = require('@app/src/services/sendEvent');

// Track traveler info interaction
await sendEventService.setSendEvent({
  userId: 12345,
  event: 'tap_traffic_camera'
});

// Track page visit
await sendEventService.setSendEvent({
  userId: 12345,
  event: 'visit_badge_page'
});

// Unrecognized events are ignored
await sendEventService.setSendEvent({
  userId: 12345,
  event: 'unknown_action' // This won't be dispatched
});
```

### Event Analytics Integration
```javascript
class UserAnalytics {
  constructor() {
    this.sendEventService = require('@app/src/services/sendEvent');
  }

  async trackUserInteraction(userId, action, context = {}) {
    try {
      // Send the primary event
      await this.sendEventService.setSendEvent({
        userId,
        event: action
      });

      // Additional analytics processing
      await this.processAnalytics(userId, action, context);
      
      return {
        success: true,
        eventTracked: action,
        category: this.getEventCategory(action)
      };
    } catch (error) {
      console.error('Error tracking user interaction:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  getEventCategory(action) {
    const travelerInfoEvents = [
      'tap_roadside', 'tap_traffic_camera', 'tap_transit_route',
      'tap_bikeshare_station', 'tap_parking_garage'
    ];
    
    const visitEvents = ['visit_badge_page', 'visit_help_desk'];
    
    if (travelerInfoEvents.includes(action)) return 'traveler_info';
    if (visitEvents.includes(action)) return 'visit_event';
    return 'untracked';
  }

  async processAnalytics(userId, action, context) {
    // Additional analytics processing
    const timestamp = new Date().toISOString();
    
    // Could integrate with other analytics services
    console.log(`Analytics: User ${userId} performed ${action} at ${timestamp}`);
    
    // Example: Update user engagement metrics
    if (context.sessionId) {
      console.log(`Session ${context.sessionId} engagement recorded`);
    }
  }

  async trackMultipleEvents(userId, events) {
    const results = [];
    
    for (const event of events) {
      try {
        const result = await this.trackUserInteraction(userId, event.action, event.context);
        results.push({
          action: event.action,
          result
        });
      } catch (error) {
        results.push({
          action: event.action,
          result: { success: false, error: error.message }
        });
      }
    }
    
    return {
      userId,
      totalEvents: events.length,
      successful: results.filter(r => r.result.success).length,
      failed: results.filter(r => !r.result.success).length,
      details: results
    };
  }
}

// Usage
const analytics = new UserAnalytics();

// Track single interaction
await analytics.trackUserInteraction(12345, 'tap_traffic_camera', {
  sessionId: 'session_abc123',
  location: { lat: 29.7604, lng: -95.3698 }
});

// Track multiple events
await analytics.trackMultipleEvents(12345, [
  { action: 'tap_roadside', context: { urgency: 'high' } },
  { action: 'visit_help_desk', context: { source: 'navigation' } },
  { action: 'tap_bikeshare_station', context: { stationId: 'station_456' } }
]);
```

### Event Monitoring and Reporting
```javascript
class EventMonitor {
  constructor() {
    this.sendEventService = require('@app/src/services/sendEvent');
    this.eventCounts = new Map();
    this.sessionEvents = new Map();
  }

  async trackWithMonitoring(userId, event, sessionId = null) {
    try {
      // Track the event
      await this.sendEventService.setSendEvent({ userId, event });
      
      // Update monitoring counters
      this.updateEventCounts(event);
      
      if (sessionId) {
        this.updateSessionEvents(sessionId, event);
      }
      
      return {
        success: true,
        event,
        userId,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Event tracking failed:', error);
      return {
        success: false,
        event,
        userId,
        error: error.message
      };
    }
  }

  updateEventCounts(event) {
    const current = this.eventCounts.get(event) || 0;
    this.eventCounts.set(event, current + 1);
  }

  updateSessionEvents(sessionId, event) {
    if (!this.sessionEvents.has(sessionId)) {
      this.sessionEvents.set(sessionId, []);
    }
    this.sessionEvents.get(sessionId).push({
      event,
      timestamp: new Date().toISOString()
    });
  }

  getEventReport() {
    const totalEvents = Array.from(this.eventCounts.values())
      .reduce((sum, count) => sum + count, 0);
      
    return {
      totalEvents,
      eventBreakdown: Object.fromEntries(this.eventCounts),
      activeSessions: this.sessionEvents.size,
      topEvents: this.getTopEvents(5)
    };
  }

  getTopEvents(limit = 5) {
    return Array.from(this.eventCounts.entries())
      .sort(([,a], [,b]) => b - a)
      .slice(0, limit)
      .map(([event, count]) => ({ event, count }));
  }

  getSessionSummary(sessionId) {
    const events = this.sessionEvents.get(sessionId) || [];
    const eventTypes = new Set(events.map(e => e.event));
    
    return {
      sessionId,
      totalEvents: events.length,
      uniqueEventTypes: eventTypes.size,
      eventTypes: Array.from(eventTypes),
      timeline: events,
      duration: events.length > 0 ? 
        new Date(events[events.length - 1].timestamp) - new Date(events[0].timestamp) : 0
    };
  }
}

// Usage
const monitor = new EventMonitor();

// Track events with monitoring
await monitor.trackWithMonitoring(12345, 'tap_traffic_camera', 'session_123');
await monitor.trackWithMonitoring(12345, 'visit_badge_page', 'session_123');

// Get monitoring reports
const report = monitor.getEventReport();
console.log('Event Report:', report);

const sessionSummary = monitor.getSessionSummary('session_123');
console.log('Session Summary:', sessionSummary);
```

## 📊 Output Examples

### Successful Event Tracking
```javascript
// Log output
"[send-event] user 12345 make event \"tap_traffic_camera\" to send"

// Return value (implicit)
// Promise resolves to undefined
```

### Event Analytics Response
```json
{
  "success": true,
  "eventTracked": "tap_traffic_camera",
  "category": "traveler_info"
}
```

### Event Monitoring Report
```json
{
  "totalEvents": 150,
  "eventBreakdown": {
    "tap_traffic_camera": 45,
    "tap_transit_route": 38,
    "visit_badge_page": 25,
    "tap_parking_garage": 22,
    "visit_help_desk": 20
  },
  "activeSessions": 12,
  "topEvents": [
    {"event": "tap_traffic_camera", "count": 45},
    {"event": "tap_transit_route", "count": 38},
    {"event": "visit_badge_page", "count": 25}
  ]
}
```

### Session Summary
```json
{
  "sessionId": "session_123",
  "totalEvents": 3,
  "uniqueEventTypes": 2,
  "eventTypes": ["tap_traffic_camera", "visit_badge_page"],
  "timeline": [
    {
      "event": "tap_traffic_camera",
      "timestamp": "2024-06-25T14:30:00.000Z"
    },
    {
      "event": "visit_badge_page", 
      "timestamp": "2024-06-25T14:32:15.000Z"
    }
  ],
  "duration": 135000
}
```

## ⚠️ Important Notes

### Event Categories and Mapping
- **Traveler Info Events:** Map-based interactions with transportation infrastructure
- **Visit Events:** Navigation to specific app sections or features
- **Unmapped Events:** Events not in the mapping table are silently ignored
- **Event Names:** Use exact string matching for event categorization

### Analytics and Monitoring
- **User ID Tracking:** All events associated with specific user identifiers
- **Event Metadata:** Original action preserved in eventMeta for detailed analysis
- **Logging:** Successful dispatches logged for monitoring and debugging
- **Silent Failures:** Unmapped events don't generate errors or logs

### Integration Considerations
- **Event Helper Dependency:** Relies on external event dispatch system
- **Simple Architecture:** Minimal processing overhead for high-frequency tracking
- **Extensibility:** Easy to add new event types by extending switch cases
- **Performance:** Lightweight service suitable for real-time tracking

### Usage Patterns
- **Mobile App Integration:** Designed for mobile app user interaction tracking
- **Real-Time Analytics:** Supports immediate event processing and analysis
- **Session Tracking:** Can be enhanced with session-based analytics
- **Behavioral Analysis:** Enables understanding of user engagement patterns

## 🔗 Related File Links

- **Send Event Helper:** `allrepo/connectsmart/tsp-api/src/helpers/send-event.js`
- **Event Controllers:** API endpoints that trigger event tracking
- **Analytics Services:** Other services that consume event data

---
*This service provides lightweight user interaction tracking with event categorization and dispatch for analytics in the TSP platform.*