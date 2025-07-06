# Send Notification Helper Documentation

## 🔍 Quick Summary (TL;DR)

Sends push notifications to users through AWS SQS with multi-language support, database persistence, and localized message handling for MaaS transportation services.

**Keywords:** notification | push-notification | AWS-SQS | multi-language | i18n | carpool | messaging | user-notification | mobile-push | cloud-messaging | transportation-alerts

**Primary Use Cases:**
- Send carpool matching notifications to riders/drivers
- Broadcast system alerts to specific user groups
- Deliver localized messages in multiple languages (en/zh/es/vi)
- Track notification delivery status in database

**Compatibility:** Node.js 14+, AWS SDK v3, Koa.js framework

## ❓ Common Questions Quick Index

- **Q: How do I send a notification?** → [Usage Methods](#usage-methods)
- **Q: What languages are supported?** → [Multi-language Support](#detailed-code-analysis)
- **Q: How are notifications stored?** → [Database Persistence](#technical-specifications)
- **Q: What if a user's language isn't supported?** → [Error Handling](#important-notes)
- **Q: How to troubleshoot failed notifications?** → [Troubleshooting](#important-notes)
- **Q: What notification types are available?** → [Notification Types](#output-examples)
- **Q: How to handle carpool-specific messages?** → [Carpool Localization](#detailed-code-analysis)
- **Q: What happens if AWS SQS fails?** → [Error Recovery](#important-notes)
- **Q: How to scale for high user volumes?** → [Performance Optimization](#improvement-suggestions)

## 📋 Functionality Overview

**Non-technical Explanation:**
Like a multilingual postal service that delivers personalized letters to people in their preferred language, this system takes a message, translates it appropriately, stores a copy for records, and delivers it to users' mobile devices through Amazon's cloud infrastructure.

**Technical Explanation:**
A notification service helper that orchestrates user-specific message delivery through AWS SQS, implementing database persistence across three tables (notifications, notification_msgs, notification_users) with automatic language detection and localized message preparation.

**Business Value:** Enables real-time user engagement for transportation services, improves user experience through native language support, and provides audit trails for compliance and analytics.

**System Context:** Core component of the TSP API notification system, integrating with authentication services, message templates, and AWS cloud messaging infrastructure.

## 🔧 Technical Specifications

**File Information:**
- **Path:** `/src/helpers/send-notification.js`
- **Type:** Helper/Utility Module
- **Language:** JavaScript (Node.js)
- **Lines:** 253
- **Complexity:** Medium-High (multi-language, async operations, database transactions)

**Dependencies:**
- `moment-timezone` (^0.5.x) - Time formatting and timezone handling [CRITICAL]
- `@aws-sdk/client-sqs` (^3.x) - AWS SQS messaging service [CRITICAL]
- `@maas/core/log` - Centralized logging system [HIGH]
- `@app/src/models/*` - Database ORM models [CRITICAL]
- `config` - Application configuration management [CRITICAL]

**Database Tables:**
- `notifications` - Main notification records
- `notification_msgs` - Localized message content
- `notification_users` - User-specific delivery tracking

**Environment Variables:**
- `AWS_REGION` - AWS service region
- `AWS_SQS_QUEUE_URL` - Target SQS queue URL
- `AWS_ACCESS_KEY_ID` - AWS credentials
- `AWS_SECRET_ACCESS_KEY` - AWS credentials

## 📝 Detailed Code Analysis

**Main Export Function:**
```javascript
async ({ userIds, titleParams, bodyParams, type, meta, silent, image }) => Promise<Object>
```

**Core Functions:**
1. **`prepareMessage()`** - Template parameter substitution with regex replacement
2. **`sendMessage()`** - AWS SQS message dispatch with database persistence
3. **`replaceStringsForCarpool()`** - Specialized carpool message localization

**Multi-language Support:**
- Supported languages: English (en), Chinese (zh), Spanish (es), Vietnamese (vi)
- Automatic language detection from user profiles
- Fallback to English for unsupported languages
- Special handling for carpool role translations (driver/rider → conductor/pasajero)

**Execution Flow:**
1. Input validation (array type checking)
2. User language detection and grouping
3. Message preparation per language group
4. Database transaction (3-table insert)
5. AWS SQS message dispatch
6. Result aggregation and return

**Error Handling:**
- Parameter validation with MaasError exceptions
- Database transaction rollback capability
- AWS SQS failure logging without blocking
- Language fallback mechanisms

## 🚀 Usage Methods

**Basic Usage:**
```javascript
const sendNotification = require('./send-notification');

const result = await sendNotification({
  userIds: [1001, 1002, 1003],
  type: NOTIFICATION_TYPE.DUO_CARPOOL_MATCHING,
  titleParams: ['John Doe'],
  bodyParams: ['Downtown', '3:30 PM'],
  meta: { tripId: 12345, driverId: 1001 },
  silent: false,
  image: 'https://example.com/carpool-icon.png'
});
// Returns: { 1001: 456, 1002: 456, 1003: 456 } - userId: notificationId mapping
```

**Carpool Matching Notification:**
```javascript
await sendNotification({
  userIds: [riderId],
  type: NOTIFICATION_TYPE.DUO_CARPOOL_MATCHING_RIDER,
  titleParams: ['New Match Found'],
  bodyParams: [driverName, pickupLocation, departureTime],
  meta: { 
    matchId: 'abc123',
    driverId: 5001,
    tripDetails: { from: 'A', to: 'B' }
  }
});
```

**Silent Background Notification:**
```javascript
await sendNotification({
  userIds: [userId],
  type: NOTIFICATION_TYPE.SYSTEM_UPDATE,
  titleParams: [],
  bodyParams: ['System maintenance scheduled'],
  meta: { maintenanceWindow: '2024-01-15T02:00:00Z' },
  silent: true  // Won't show in notification center when app is backgrounded
});
```

## 📊 Output Examples

**Successful Execution:**
```javascript
// Input
{
  userIds: [1001, 1002],
  type: 101,
  titleParams: ['Driver John'],
  bodyParams: ['5 minutes', 'Main St'],
  meta: { tripId: 789 }
}

// Output
{
  1001: 456,  // userId: notificationId in database
  1002: 456
}

// Database Records Created:
// notifications table: id=456, notification_type=101, msg_data='{"tripId":789}'
// notification_msgs table: id=789, notification_id=456, msg_title='Driver John is arriving'
// notification_users table: user_id=1001, notification_msg_id=789, send_status='sent'
```

**Multi-language Processing:**
```javascript
// Users with different languages get localized messages
// User 1001 (English): "Driver John is 5 minutes away"
// User 1002 (Spanish): "El conductor John está a 5 minutos"
// User 1003 (Chinese): "司機 John 還有5分鐘到達"
```

**Error Scenarios:**
```javascript
// Invalid parameters
throw new MaasError(ERROR_BAD_REQUEST_PARAMS, 'error', 'The parameters are not array');

// AWS SQS failure (logged but doesn't throw)
// Log: "Send notification Id:456 Error:NetworkingError: socket hang up"
```

## ⚠️ Important Notes

**Security Considerations:**
- AWS credentials must be properly configured in environment
- Meta data is stored as JSON string in database (validate before insertion)
- User ID validation should be performed by calling services
- No rate limiting implemented - implement upstream

**Performance Gotchas:**
- Parallel user language detection can be expensive with many users
- Database transactions are not atomic across all operations
- AWS SQS calls are synchronous - consider batching for high volume
- Memory usage grows linearly with user count

**Troubleshooting Steps:**
1. **No notifications received:** Check AWS SQS queue configuration and credentials
2. **Wrong language messages:** Verify user profile `device_language` field format
3. **Database errors:** Check database connectivity and table schema
4. **Missing message content:** Verify `NOTIFICATION_MSG_LIST` static data completeness

**Common Issues:**
- Language code must be 2-character format (extracts first 2 chars automatically)
- Silent notifications still create database records
- Notification expiry is hardcoded to 30 days
- Type aliases are applied before database storage

## 🔗 Related File Links

**Dependencies:**
- `/src/models/AuthUsers.js` - User profile and language detection
- `/src/models/Notifications.js` - Main notification records
- `/src/models/NotificationMsgs.js` - Localized message storage
- `/src/models/NotificationUsers.js` - User delivery tracking
- `/src/static/notification-msg.js` - Message templates and translations
- `/src/static/defines.js` - System constants and enums

**Configuration:**
- `/config/default.js` - AWS and application settings
- `/src/static/error-code.js` - Error definitions and codes

**Usage Examples:**
- Controllers using this helper for user notifications
- Carpool matching services for ride alerts
- System maintenance notification broadcasters

## 📈 Use Cases

**Daily Operations:**
- Ride matching notifications for carpool users
- System maintenance alerts to active users
- Promotional messages for specific user segments
- Emergency notifications for transportation disruptions

**Development Scenarios:**
- Testing multi-language notification delivery
- Debugging notification delivery failures
- Performance testing with large user groups
- Integration testing with AWS services

**Integration Patterns:**
- Event-driven notifications from business logic
- Scheduled notifications via cron jobs
- Real-time notifications from WebSocket events
- Batch notifications for user segments

## 🛠️ Improvement Suggestions

**Performance Optimization:**
- Implement SQS batch messaging for >10 users (reduces API calls by 80%)
- Add Redis caching for user language preferences
- Use database connection pooling for concurrent operations
- Implement async/await batching for database operations

**Feature Enhancements:**
- Add notification scheduling capabilities
- Implement push notification analytics and delivery confirmation
- Support for rich media notifications (images, actions)
- Add notification preference management per user

**Code Quality:**
- Extract language handling into separate service
- Add comprehensive unit tests for all functions
- Implement proper database transaction management
- Add input sanitization and validation middleware

## 🏷️ Document Tags

**Keywords:** push-notification, AWS-SQS, multi-language, i18n, mobile-messaging, user-notification, carpool-alerts, cloud-messaging, notification-service, localization, database-persistence, async-processing, transportation-communication

**Technical Tags:** #notification #aws #sqs #i18n #mobile #push #messaging #helper #utility #async #database #orm #localization #carpool #transportation

**Target Roles:** Backend developers (intermediate), DevOps engineers (AWS), QA engineers (integration testing), Product managers (notification features)

**Difficulty Level:** ⭐⭐⭐⭐ (4/5) - Complex due to multi-language handling, AWS integration, database transactions, and async coordination

**Maintenance Level:** Medium - Regular updates needed for new languages, notification types, and AWS SDK versions

**Business Criticality:** High - Core user engagement feature affecting user experience and retention

**Related Topics:** AWS services, mobile app development, internationalization, database design, message queuing, user communication systems