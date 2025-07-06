# Notification Service Test Suite

## Overview
Comprehensive test suite for the notification service functionality that validates both the helper function and service layer for sending push notifications to users. The tests verify message delivery, parameter handling, database record creation, and response formatting across different notification scenarios.

## File Location  
`/test/testNotification.js`

## Technical Analysis

### Core Services Under Test
The test validates two notification approaches:
```javascript
const sendNotification = require('@app/src/helpers/send-notification');
const service = require('@app/src/services/sendNotification');
```

The helper provides simplified notification sending while the service offers more granular control and additional features.

### Dependencies
- `@maas/core/bootstrap` - Application bootstrap and environment setup
- `chai` - Assertion library with expect interface for validation
- `@app/src/helpers/send-notification` - Notification helper function
- `@app/src/services/sendNotification` - Core notification service layer

### Test Architecture

#### Common Test Parameters
```javascript
const userIds = [1003];           // Target user array
const titleParams = ['title'];    // Notification title parameters
const bodyParams = ['body'];      // Notification body parameters  
const type = 1;                   // Notification type identifier
const meta = {};                  // Additional metadata object
const silent = false;             // Sound/vibration setting
const image = '';                 // Optional image URL
```

#### Parameter Validation Patterns
Both helper and service tests use identical parameter sets to ensure consistency across the notification infrastructure.

### Helper Function Tests

#### Standard Notification Test
```javascript
it('normal happy case', async () => {
  const result = await sendNotification({
    userIds,
    titleParams,
    bodyParams,
    type,
    meta,
    silent,
    image,
  });
  expect(result).to.be.an('object');
  expect(result).to.include.keys([1003]);
});
```

The helper function returns an object keyed by user ID, providing notification delivery status per recipient.

#### Image-Optional Test
```javascript
it('without image', async () => {
  const result = await sendNotification({
    userIds,
    titleParams,
    bodyParams,
    type,
    meta,
    silent,
  });
  expect(result).to.be.an('object');
  expect(result).to.include.keys([1003]);
});
```

Tests notification delivery when image parameter is omitted, ensuring backward compatibility.

### Service Layer Tests

#### Standard Service Test
```javascript
it('service normal happy case', async () => {
  const result = await service.sendNotification(
    userIds,
    type,
    titleParams,
    bodyParams,
    meta,
    'en',
    silent,
    false,
    image,
  );
  expect(result).to.be.an('array');
  expect(result.length).to.above(0);
  expect(result[0]).to.be.an('object');
  expect(result[0]).to.include.keys(['notificationId']);
  expect(result[0]).to.include.keys(['notificationMsgId']);
  expect(result[0]).to.include.keys(['notificationUserId']);
});
```

The service layer returns an array of objects containing database record identifiers for tracking notification delivery.

#### Response Structure Validation
Service responses include three key identifiers:
- `notificationId` - Primary notification record ID
- `notificationMsgId` - Message content record ID  
- `notificationUserId` - User-specific delivery record ID

### Parameter Differences

#### Helper vs Service Function Signatures
**Helper Function:**
```javascript
sendNotification({
  userIds,
  titleParams, 
  bodyParams,
  type,
  meta,
  silent,
  image
})
```

**Service Function:**
```javascript
service.sendNotification(
  userIds,           // User ID array
  type,             // Notification type
  titleParams,      // Title parameters
  bodyParams,       // Body parameters
  meta,             // Metadata object
  'en',             // Language code
  silent,           // Silent flag
  false,            // Additional boolean flag
  image             // Image URL (optional)
)
```

## Usage/Integration

### Helper Function Usage
The helper function provides a simplified interface for basic notification needs:
- Single object parameter with named properties
- Returns user-keyed result object
- Suitable for simple notification scenarios

### Service Layer Usage  
The service function offers more control and features:
- Positional parameters for explicit control
- Language specification support
- Additional configuration flags
- Database record tracking via returned IDs
- Integration with notification management systems

### Database Integration
The service layer creates records in multiple tables:
- `notification` - Primary notification record
- `notification_msg` - Message content storage
- `notification_user` - User-specific delivery tracking

## Code Examples

### Basic Helper Usage
```javascript
const result = await sendNotification({
  userIds: [1003, 1004],
  titleParams: ['Welcome'],
  bodyParams: ['Thank you for joining'],
  type: 1,
  meta: { campaign_id: 'welcome_2024' },
  silent: false,
  image: 'https://example.com/welcome.png'
});

// Result format: { 1003: status, 1004: status }
```

### Service Layer Usage
```javascript
const results = await service.sendNotification(
  [1003, 1004],          // userIds
  1,                     // type
  ['Welcome'],           // titleParams
  ['Thank you'],         // bodyParams  
  { source: 'app' },     // meta
  'en-US',              // language
  false,                // silent
  false,                // additional flag
  'image_url'           // image
);

// Result format: [
//   {
//     notificationId: 123,
//     notificationMsgId: 456, 
//     notificationUserId: 789
//   }
// ]
```

### Error Handling Pattern
```javascript
try {
  const result = await sendNotification({
    userIds: [invalidUserId],
    titleParams: ['Test'],
    bodyParams: ['Test message'],
    type: 1,
    meta: {},
    silent: false
  });
} catch (error) {
  console.error('Notification failed:', error.message);
}
```

## Integration Points

### External Services
- **Push Notification Providers**: Apple Push Notification Service (APNS), Firebase Cloud Messaging (FCM)
- **Database Systems**: MySQL for notification record persistence
- **Localization Services**: Multi-language message template support

### System Dependencies
- **User Management**: Integration with user authentication and device registration
- **Message Templates**: Localized notification content management
- **Delivery Tracking**: Notification status and delivery confirmation

### Monitoring and Analytics
- **Delivery Metrics**: Success/failure rates per notification type
- **User Engagement**: Open rates and interaction tracking  
- **Performance Monitoring**: Response times and throughput analysis

The notification test suite ensures reliable message delivery across both simplified helper functions and full-featured service implementations, supporting the platform's comprehensive user engagement and communication requirements.