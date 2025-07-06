# Send Notification Service Test Suite

## Overview
Focused test suite for the notification service layer that validates the core notification delivery functionality, database record creation, and notification system integration. This test ensures the service layer properly handles notification requests and maintains proper database state for notification tracking and delivery confirmation.

## File Location
`/test/testSendNotification.js`

## Technical Analysis

### Core Service Under Test
```javascript
const { sendNotification } = require('@app/src/services/sendNotification');
```

This service function handles the complete notification delivery process including database record creation, message queuing, and delivery status tracking.

### Dependencies
- `chai` - Assertion library with assert interface for validation
- `@maas/core/mysql` - MySQL database connection for portal operations
- `@app/src/services/sendNotification` - Core notification service implementation

### Test Architecture

#### Database Integration Pattern
```javascript
const knex = require('@maas/core/mysql')('portal');
```

Uses direct MySQL connection to validate database operations and ensure proper record creation across notification-related tables.

#### Dynamic User Selection
```javascript
let userId = null;
before(async () => {
  const ids = await knex('auth_user').select('id').limit(1);
  userId = ids[0].id;
});
```

Dynamically selects a valid user ID from the database, ensuring tests work with actual user data rather than hardcoded values.

### Notification Parameter Configuration

#### Standard Notification Parameters
```javascript
const notificationType = 1;         // Notification type identifier
const titleParams = 'test';         // Notification title content
const bodyParams = 'test';          // Notification body content
const meta = {};                    // Metadata object for additional context
const language = 'en-US';          // User language preference
const silent = false;              // Sound/vibration setting
```

These parameters represent the complete notification specification required for delivery.

### Database Record Validation

#### Multi-Table Verification
```javascript
it('send one notification', async () => {
  const results = await sendNotification(
    [userId],
    notificationType,
    titleParams,
    bodyParams,
    meta,
    language,
    silent,
  );
  
  assert.equal(results.length, 1, 'Result should be 1.');
  
  for (const result of results) {
    // Validate notification record
    const notification = await knex('notification')
      .select()
      .where({ id: result.notificationId });
    assert.equal(notification.length, 1, 'Result should be 1.');
    
    // Validate notification message record
    const notificationMsg = await knex('notification_msg')
      .select()
      .where({ id: result.notificationMsgId });
    assert.equal(notificationMsg.length, 1, 'Result should be 1.');
    
    // Validate notification user record
    const notificationUser = await knex('notification_user')
      .select('user_id')
      .where({ id: result.notificationUserId });
    assert.equal(notificationUser.length, 1, 'Result should be 1.');
    assert.equal(notificationUser[0].user_id, userId, 'Should equal');
  }
});
```

## Usage/Integration

### Service Function Signature
```javascript
await sendNotification(
  userIds,           // Array of target user IDs
  notificationType,  // Notification type (1-N)
  titleParams,       // Title content or parameters
  bodyParams,        // Body content or parameters
  meta,              // Additional metadata object
  language,          // User language code
  silent             // Silent notification flag
);
```

### Database Schema Integration
The service creates records in three related tables:

#### notification Table
- Primary notification record with type, metadata, and timing information
- Referenced by `result.notificationId`

#### notification_msg Table  
- Message content storage including title, body, and localization
- Referenced by `result.notificationMsgId`

#### notification_user Table
- User-specific delivery tracking and status information
- Referenced by `result.notificationUserId`
- Contains foreign key to `auth_user.id`

### Response Structure
```javascript
// Service returns array of objects with database record identifiers
[
  {
    notificationId: 123,        // Primary notification record ID
    notificationMsgId: 456,     // Message content record ID
    notificationUserId: 789     // User delivery record ID
  }
]
```

## Code Examples

### Basic Notification Sending
```javascript
const notificationResults = await sendNotification(
  [1003, 1004],                    // Multiple users  
  1,                               // Notification type
  'Welcome to MaaS',              // Title
  'Thank you for joining our platform',  // Body
  { campaign: 'onboarding' },     // Metadata
  'en-US',                        // Language
  false                           // Not silent
);

console.log(`Sent ${notificationResults.length} notifications`);
```

### Database Record Verification
```javascript
// Verify notification was properly created
for (const result of notificationResults) {
  // Check primary notification record
  const notification = await knex('notification')
    .select('*')
    .where({ id: result.notificationId })
    .first();
  
  console.log('Notification created:', notification.created_at);
  
  // Check message content
  const message = await knex('notification_msg')
    .select('title', 'body')
    .where({ id: result.notificationMsgId })
    .first();
  
  console.log('Message:', message.title, message.body);
  
  // Check user delivery record
  const userDelivery = await knex('notification_user')
    .select('user_id', 'status')
    .where({ id: result.notificationUserId })
    .first();
  
  console.log('User delivery:', userDelivery.user_id, userDelivery.status);
}
```

### Error Handling Pattern
```javascript
try {
  const results = await sendNotification(
    [invalidUserId],
    1,
    'Test Title',
    'Test Body', 
    {},
    'en-US',
    false
  );
} catch (error) {
  console.error('Notification failed:', error.message);
  
  // Check if partial database records were created
  const orphanedRecords = await knex('notification')
    .where('created_at', '>', new Date(Date.now() - 5000));
  
  if (orphanedRecords.length > 0) {
    console.warn('Orphaned notification records detected');
  }
}
```

### Batch Notification Processing
```javascript
const batchNotify = async (userIds, message) => {
  const batchSize = 100;
  const results = [];
  
  for (let i = 0; i < userIds.length; i += batchSize) {
    const batch = userIds.slice(i, i + batchSize);
    const batchResults = await sendNotification(
      batch,
      1,
      message.title,
      message.body,
      message.meta,
      'en-US',
      false
    );
    results.push(...batchResults);
  }
  
  return results;
};
```

## Integration Points

### Database Transaction Management
- **Atomic Operations**: Ensures all notification records are created together
- **Foreign Key Integrity**: Maintains referential integrity across related tables
- **Error Recovery**: Proper rollback handling for failed notifications

### Notification Delivery System
- **Push Notification Services**: Integration with APNS, FCM for mobile delivery
- **Email Services**: SMTP integration for email notifications
- **SMS Services**: Twilio integration for text message delivery

### User Management Integration
- **Authentication System**: Validates user existence and permissions
- **Language Preferences**: Respects user language settings for localization
- **Notification Preferences**: Honors user opt-out and preference settings

### Monitoring and Analytics
- **Delivery Tracking**: Database records enable delivery status monitoring
- **Performance Metrics**: Notification success rates and timing analysis
- **User Engagement**: Click-through and interaction tracking capabilities

### Message Queue Integration
- **Asynchronous Processing**: Background job queuing for large notification batches
- **Retry Logic**: Failed notification retry mechanisms
- **Priority Handling**: Different notification types with varying urgency levels

This test suite ensures the notification service maintains data integrity while providing reliable notification delivery across multiple channels and user segments, supporting the platform's comprehensive user engagement and communication requirements.