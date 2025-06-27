# NotificationTypes Model Documentation

## 📋 Model Overview
- **Purpose:** Defines types/categories of notifications for message classification and management
- **Table/Collection:** notification_type
- **Database Type:** MySQL
- **Relationships:** 
  - hasMany: Notifications (via notification_type foreign key)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| name | varchar(512) | Yes | Notification type name/description |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified in schema
- **Unique Constraints:** None
- **Default Values:** None

## 📝 Usage Examples
```javascript
// Get all notification types
const types = await NotificationTypes.query();

// Create a new notification type
const newType = await NotificationTypes.query().insert({
  name: 'Trip Reminder'
});

// Find specific notification type
const tripType = await NotificationTypes.query()
  .where('name', 'like', '%trip%')
  .first();

// Get type with related notifications
const typeWithNotifications = await NotificationTypes.query()
  .withGraphFetched('notifications')
  .findById(1);
```

## 🔗 Related Models
- `Notifications` - One-to-many relationship for notifications of this type
- `IncentiveNotifyQueue` - References notification types for queued messages
- `IncidentEventNotificationQueue` - Uses notification types for event notifications

## 📌 Important Notes
- Simple lookup table for categorizing notification messages
- Used as foreign key reference in multiple notification-related tables
- Types help organize and filter different kinds of system notifications
- Common types might include: trip alerts, promotional messages, system notifications, etc.

## 🏷️ Tags
**Keywords:** notifications, messaging, types, categories, lookup
**Category:** #model #database #notifications #reference-data