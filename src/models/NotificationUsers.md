# Model Documentation: NotificationUsers

## 📋 Model Overview
- **Purpose:** Manages user notification preferences and settings
- **Table/Collection:** notification_user
- **Database Type:** MySQL
- **Relationships:** Not defined in model (likely references auth_users)

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| *Schema not defined in model file* | - | - | Table structure exists in database |

## 🔑 Key Information
- **Primary Key:** Likely id (standard convention)
- **Indexes:** Database-defined
- **Unique Constraints:** Database-defined
- **Default Values:** Database-defined

## 📝 Usage Examples
```javascript
// Get notification settings for a user
const notifications = await NotificationUsers.query()
  .where('user_id', userId);

// Update notification preferences
await NotificationUsers.query()
  .patch({ push_enabled: true, email_enabled: false })
  .where('user_id', userId);

// Create notification settings for new user
const settings = await NotificationUsers.query().insert({
  user_id: userId,
  // other notification preferences
});

// Delete notification settings
await NotificationUsers.query()
  .delete()
  .where('user_id', userId);
```

## 🔗 Related Models
- AuthUsers - user_id likely references auth_users table
- Notifications - may relate to actual notification records

## 📌 Important Notes
- Uses MySQL 'portal' connection
- Minimal model definition - schema is database-driven
- Part of Objection.js ORM system
- Likely stores user preferences for push, email, SMS notifications

## 🏷️ Tags
**Keywords:** notifications, user preferences, settings, alerts
**Category:** #model #database #notifications #mysql

---