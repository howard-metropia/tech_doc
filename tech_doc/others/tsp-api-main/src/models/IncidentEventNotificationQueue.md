# IncidentEventNotificationQueue Model Documentation

## 📋 Model Overview
- **Purpose:** Manages notification queue for incident events
- **Table/Collection:** incident_event_notification_queue
- **Database Type:** MySQL
- **Relationships:** Links to incident events and notification system

## 🔧 Schema Definition
Schema details not explicitly defined in model file. This is a queue management table for incident-related notifications.

## 🔑 Key Information
- **Primary Key:** Likely id (standard MySQL convention)
- **Indexes:** Not defined in model (handled at database level)
- **Unique Constraints:** Not defined in model
- **Default Values:** Not defined in model

## 📝 Usage Examples
```javascript
// Query pending notifications
const pendingNotifications = await IncidentEventNotificationQueue.query()
  .where('status', 'pending');

// Add new notification to queue
const notification = await IncidentEventNotificationQueue.query()
  .insert({
    incident_id: 12345,
    user_id: 67890,
    notification_type: 'incident_alert',
    status: 'pending'
  });

// Process notification queue
const nextNotification = await IncidentEventNotificationQueue.query()
  .where('status', 'pending')
  .orderBy('created_at', 'asc')
  .first();
```

## 🔗 Related Models
- **IncidentsEvent** - Source of incident data for notifications
- **User models** - Recipients of notifications
- **Notification models** - General notification system
- **Alert models** - Real-time alert processing

## 📌 Important Notes
- Missing Model import from 'objection' (implementation issue)
- Queue-based notification processing for scalability
- Likely includes status tracking (pending, sent, failed)
- Connected to 'portal' MySQL database
- Critical for incident response and user safety alerts
- Supports asynchronous notification delivery

## 🏷️ Tags
**Keywords:** incident, notification, queue, alert, event, async
**Category:** #model #database #mysql #notification #queue