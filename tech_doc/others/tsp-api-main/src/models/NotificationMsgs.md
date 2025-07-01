# NotificationMsgs Model

## 📋 Model Overview
- **Purpose:** Stores notification messages for user communication
- **Table/Collection:** notification_msg
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
const messages = await NotificationMsgs.query().where('user_id', 123);

// Get unread messages
const unread = await NotificationMsgs.query().where('read_status', false);
```

## 🔗 Related Models
- No explicit relationships defined
- Part of notification system

## 📌 Important Notes
- Minimal model with only table name definition
- Part of user notification and messaging system
- Uses Objection.js ORM with MySQL portal database

## 🏷️ Tags
**Keywords:** notification, message, communication, user
**Category:** #model #database #notification #message