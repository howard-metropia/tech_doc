# Send Notification Helper

## Overview
**File**: `src/helpers/send-notification.js`  
**Type**: Notification Utility  
**Purpose**: Sends push notifications via AWS SQS with multi-language support and database persistence

## Core Function

### Notification Sending
```javascript
module.exports = async ({
  userIds,
  titleParams,
  bodyParams,
  type,
  meta,
  silent,
  image,
}) => {
  // Group users by language
  // Generate localized messages
  // Send via SQS and store in database
}
```

## Language Support

### User Language Grouping
```javascript
const langUsers = {
  en: [],
  zh: [],
  es: [],
  vi: [],
};
```

### Language Detection
```javascript
const lang = userProfile.device_language
  ? userProfile.device_language.slice(0, 2) // First two characters
  : 'en'; // Default to English
```

## Message Preparation

### Template Processing
```javascript
const prepareMessage = (lang, mode, type, params) => {
  let data = NOTIFICATION_MSG_LIST?.[mode]?.[type]?.[lang] ?? '';
  if (data && params?.length) {
    const replaceStrings = data.match(/%(\w+)%/g);
    replaceStrings.forEach((el) => {
      data = data.replace(el, params[i++]);
    });
  }
  return data;
};
```

### Special Case Handling
```javascript
// Carpool cancellation message translation
const replaceStringsForCarpool = (lang, targetString) => {
  // Handle role translation (driver/rider)
  // Handle verb tense translation (you sent/sent you)
  return translatedMessage;
};
```

## Database Integration

### Tables Used
- **Notifications**: Main notification records
- **NotificationMsgs**: Localized message content
- **NotificationUsers**: User-specific notification tracking

### Database Flow
```javascript
// 1. Create notification record
const notification = await Notifications.query().insert({
  msg_data: metaString,
  started_on: curTime,
  ended_on: endTime,
  silent: silent ? 'T' : 'F',
  notification_type: type,
});

// 2. Create message record
const notificationMsg = await NotificationMsgs.query().insert({
  notification_id: notificationId,
  msg_title: title,
  msg_body: body,
  lang,
});

// 3. Create user tracking records
await NotificationUsers.query().insert({
  notification_msg_id: notificationMsg.id,
  user_id: userId,
  send_status: NOTIFY_USER_STATUS.NOTIFY_STATUS_SENT,
});
```

## SQS Integration

### Message Format
```javascript
{
  action: 'cloud_message',
  data: {
    silent: false,
    notification_type: type,
    user_list: userIds,
    title: 'Notification Title',
    body: 'Notification Body',
    meta: {},
    notification_id: 12345,
    image: 'https://example.com/image.jpg'
  }
}
```

### AWS SQS Sending
```javascript
const client = new SQSClient({ region: awsConfig.region });
await client.send(
  new SendMessageCommand({
    MessageBody: JSON.stringify(message),
    QueueUrl: awsConfig.sqs.queueUrl,
  })
);
```

## Notification Types

### Special Handling
- **INSTANT_CARPOOL_NOTIFY_RIDER**: Three sub-types based on status
- **DUO_CARPOOL_CANCELLED_WITH_REASON**: Carpool cancellation handling
- **Standard Types**: Generic title/body template processing

### Type-Specific Logic
```javascript
if (type === NOTIFICATION_TYPE.INSTANT_CARPOOL_NOTIFY_RIDER) {
  title = NOTIFICATION_MSG_LIST.title[type]?.[meta.status]?.[lang] ?? '';
  body = NOTIFICATION_MSG_LIST.body[type]?.[meta.status]?.[lang] ?? '';
  meta.title = title;
  meta.body = body;
}
```

## Parameters

### Required Parameters
- **userIds**: Array of user IDs to notify
- **type**: Notification type identifier
- **meta**: Metadata object for notification

### Optional Parameters
- **titleParams**: Parameters for title template
- **bodyParams**: Parameters for body template
- **silent**: Boolean for silent notifications
- **image**: Image URL for rich notifications

## Error Handling

### Input Validation
```javascript
if (
  !Array.isArray(userIds) ||
  (titleParams && !Array.isArray(titleParams)) ||
  (bodyParams && !Array.isArray(bodyParams))
) {
  throw new MaasError(ERROR_BAD_REQUEST_PARAMS);
}
```

### Error Recovery
- **Database Errors**: Logged but don't stop processing
- **SQS Errors**: Logged with warning level
- **Language Errors**: Falls back to default language

## Usage Examples

### Basic Notification
```javascript
const sendNotification = require('./send-notification');

await sendNotification({
  userIds: [12345, 67890],
  type: NOTIFICATION_TYPE.TRIP_COMPLETED,
  titleParams: ['Austin Metro'],
  bodyParams: ['5.2 miles', '$2.50'],
  meta: {
    trip_id: 'abc123',
    amount: 250
  }
});
```

### Silent Notification
```javascript
await sendNotification({
  userIds: [12345],
  type: NOTIFICATION_TYPE.DATA_UPDATE,
  meta: { update_type: 'schedule' },
  silent: true
});
```

### Rich Notification with Image
```javascript
await sendNotification({
  userIds: [12345],
  type: NOTIFICATION_TYPE.PROMOTION,
  titleParams: ['50% Off'],
  bodyParams: ['Transit passes'],
  meta: { promotion_id: 'promo123' },
  image: 'https://cdn.example.com/promo.jpg'
});
```

## Localization

### Supported Languages
- **en**: English (default)
- **zh**: Chinese
- **es**: Spanish
- **vi**: Vietnamese

### Message Templates
- **NOTIFICATION_MSG_LIST**: Centralized message templates
- **Parameter Substitution**: `%param%` placeholder replacement
- **Fallback**: Empty string if translation missing

## Dependencies

### Models
- `AuthUsers`: User profile and language preferences
- `Notifications`: Main notification records
- `NotificationMsgs`: Localized message content
- `NotificationUsers`: User notification tracking

### External Services
- **AWS SQS**: Push notification delivery
- **Moment**: Date/time formatting
- **Static Definitions**: Notification types and constants

## Performance Considerations

### Language Grouping
- **Parallel Processing**: Uses Promise.all for language groups
- **Batch Queries**: Efficient user language lookup
- **Memory Efficiency**: Groups users to minimize messages

### Database Optimization
- **Batch Inserts**: Could be optimized for large user lists
- **Indexes**: Ensure proper indexing on user_id, notification_id
- **Cleanup**: Consider retention policies for old notifications

## Monitoring

### Logging
```javascript
logger.info(
  `Send notification Id:${notificationId} Type:${type} UserIds:${userIds} Title:${title} Body:${body} Meta:${metaString}`
);
```

### Metrics to Track
- **Delivery Rate**: Successful notifications sent
- **Language Distribution**: Usage by language
- **Type Popularity**: Most common notification types
- **Processing Time**: Time to process and send

## Configuration Requirements

### AWS Configuration
```javascript
vendor: {
  aws: {
    region: 'us-east-1',
    sqs: {
      queueUrl: 'https://sqs.us-east-1.amazonaws.com/123456789/notifications'
    }
  }
}
```

### Notification Templates
- **NOTIFICATION_MSG_LIST**: Message template configuration
- **Language Files**: Per-language template definitions
- **Type Definitions**: Notification type constants

## Security Considerations

### Data Privacy
- **User Language**: Logged for debugging
- **Notification Content**: May contain sensitive information
- **Access Control**: Restrict notification sending permissions

### Input Validation
- **Array Validation**: Ensures proper parameter types
- **User Existence**: Validates user IDs exist
- **Content Sanitization**: Consider message content validation

## Testing

### Unit Tests
```javascript
// Mock AWS SQS
jest.mock('@aws-sdk/client-sqs');

// Mock database models
jest.mock('@app/src/models/AuthUsers');
jest.mock('@app/src/models/Notifications');
```

### Integration Tests
- **Multi-Language**: Test all supported languages
- **Database Persistence**: Verify complete data flow
- **SQS Integration**: Test actual AWS integration
- **Error Scenarios**: Test failure handling