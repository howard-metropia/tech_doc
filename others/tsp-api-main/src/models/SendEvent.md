# SendEvent Model Documentation

## 📋 Model Overview
- **Purpose:** Flexible event storage for tracking various system events and user actions
- **Table/Collection:** send_event
- **Database Type:** MongoDB
- **Relationships:** None (generic event logging)

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| event_type | String | No | Type of event being logged |
| user_id | Mixed | No | Associated user identifier |
| timestamp | Date | No | When event occurred |
| data | Object | No | Event-specific data payload |
| session_id | String | No | User session identifier |
| ip_address | String | No | Client IP address |
| user_agent | String | No | Client user agent string |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** None explicitly defined (relies on _id)
- **Unique Constraints:** None
- **Default Values:** MongoDB auto-generates _id and timestamps

## 📝 Usage Examples
```javascript
// Log user action event
const event = new SendEvent({
  event_type: 'user_login',
  user_id: 12345,
  timestamp: new Date(),
  data: { 
    login_method: 'email',
    ip_address: '192.168.1.1'
  }
});
await event.save();

// Query events by type
const loginEvents = await SendEvent.find({
  event_type: 'user_login'
}).sort({ timestamp: -1 });
```

## 🔗 Related Models
- None - generic event logging model used across the system

## 📌 Important Notes
- Uses flexible schema (strict: false) to accommodate various event types
- No predefined field validation - relies on application logic
- Suitable for analytics, debugging, and audit trails
- Consider adding indexes based on query patterns for performance

## 🏷️ Tags
**Keywords:** events, logging, analytics, flexible-schema
**Category:** #model #database #logging #events