# IncentiveNotifyQueue Model

## 📋 Model Overview
- **Purpose:** Manages queue for incentive notifications to be sent to users
- **Table/Collection:** incentive_notify_queue
- **Database Type:** MySQL (portal)
- **Relationships:** None defined

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id`)
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const notifications = await IncentiveNotifyQueue.query().where('status', 'pending');

// Get all queued notifications
const allNotifications = await IncentiveNotifyQueue.query();
```

## 🔗 Related Models
- No explicit relationships defined
- Likely related to user and incentive models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of incentive notification system
- Uses Objection.js ORM with MySQL portal database
- Queue-based architecture for async notification processing

## 🏷️ Tags
**Keywords:** incentive, notification, queue, async, messaging
**Category:** #model #database #incentive #notification #queue