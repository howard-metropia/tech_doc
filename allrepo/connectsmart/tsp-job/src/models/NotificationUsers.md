# NotificationUsers Model

## Overview
User-specific notification management model for the TSP Job system. Handles individual notification targeting, delivery preferences, and user communication tracking.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class NotificationUsers extends Model {
  static get tableName() {
    return 'notification_users';
  }
}
module.exports = NotificationUsers.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `notification_users`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- User-specific notification targeting
- Delivery preference management
- Communication tracking
- Personalized messaging

## Key Features
- Individual user targeting
- Preference-based delivery
- Multi-channel support
- Delivery status tracking

## Notification Channels
- **Push Notifications**: Mobile app alerts
- **Email**: HTML and text messages
- **SMS**: Text messaging
- **In-App**: Application notifications

## Integration Points
- **AuthUsers**: User identification
- **Notifications**: Notification templates
- **UserConfig**: User preferences
- **NotificationRecord**: Delivery tracking

## Usage Context
Used for personalized communication, targeted alerts, preference-based messaging, and user engagement optimization.

## Targeting Features
- User segmentation support
- Preference filtering
- Behavioral targeting
- Geographic targeting

## Performance Optimization
- Efficient user lookups
- Batch notification processing
- Optimized delivery queues
- Scalable for high volumes

## Related Models
- AuthUsers: User association
- Notifications: Message templates
- NotificationRecord: Delivery logs
- UserConfig: Preferences

## API Integration
- User notification endpoints
- Preference management APIs
- Delivery tracking services
- Personalization features

## Development Notes
- User privacy focused
- Scalable messaging system
- Multi-channel optimization
- Analytics integration support