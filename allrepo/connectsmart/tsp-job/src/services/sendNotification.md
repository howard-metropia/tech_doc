# Send Notification Service

## Overview

The Send Notification service manages comprehensive push notification delivery through database storage and queue processing, supporting multilingual messaging, metadata, and delivery tracking.

## Service Information

- **Service Name**: Send Notification
- **File Path**: `/src/services/sendNotification.js`
- **Type**: Notification Delivery Service
- **Dependencies**: MySQL, Queue Service, Moment.js

## Functions

### sendNotification(users, notificationType, title, body, meta, lang, silent, noPush, image)

Comprehensive notification delivery with database persistence and queue integration.

**Purpose**: Sends notifications to users with complete tracking and delivery management
**Parameters**:
- `users` (array|number): User ID(s) to receive notification
- `notificationType` (number): Notification category identifier
- `title` (string): Notification title/headline
- `body` (string): Notification message content
- `meta` (object): Additional metadata for notification
- `lang` (string): Language code for localization
- `silent` (boolean): Silent notification flag
- `noPush` (boolean): Database-only mode (no push delivery)
- `image` (string): Optional notification image URL

**Returns**: Array of notification record IDs

## Database Schema

### Notification Tables
- **notification**: Main notification record
- **notification_msg**: Message content and language
- **notification_user**: User-specific delivery tracking

### Data Structure
```javascript
// notification table
{
  msg_data: JSON.stringify(meta),
  ended_on: sevendays,      // 7 days expiration
  started_on: now,          // Current timestamp
  silent: 'T'/'F',          // Silent flag
  notification_type: type   // Category ID
}

// notification_msg table
{
  notification_id: notifId,
  msg_title: title,
  msg_body: body,
  lang: lang.replace('-', '_')  // Underscore format
}

// notification_user table
{
  notification_msg_id: notifmId,
  user_id: userId,
  send_status: 0  // Initially pending
}
```

## Message Processing

### Language Handling
- **Format Conversion**: Dash to underscore (en-us → en_us)
- **Storage Format**: Database uses underscore format
- **Localization**: Supports all language variants

### Metadata Management
- **JSON Storage**: Serializes metadata objects
- **Flexible Structure**: Supports any metadata format
- **Query Support**: Enables metadata-based filtering

### Expiration Management
- **Default Duration**: 7 days from creation
- **Automatic Cleanup**: System handles expired notifications
- **Timezone**: UTC-based expiration timestamps

## Queue Integration

### Message Structure
```javascript
const msg = {
  silent: false,
  user_list: [userId],
  notification_type: notificationType,
  ended_on: now,
  title,
  body,
  notification_id: notifId,
  meta,
  image  // Optional
};
```

### Delivery Modes
- **Normal Mode**: Database storage + push delivery via queue
- **Database Only**: noPush=true stores without sending
- **Silent Mode**: Delivered without sound/vibration

### Queue Task
- **Task Type**: 'cloud_message'
- **Payload**: Complete notification message
- **Async Processing**: Non-blocking delivery

## Status Tracking

### Send Status Values
- **0**: Pending/queued for delivery
- **2**: Successfully sent to queue

### Delivery Flow
1. **Database Insert**: Creates notification records
2. **Queue Submission**: Sends to cloud messaging queue
3. **Status Update**: Marks as sent (status = 2)
4. **Response**: Returns record IDs for tracking

## Error Handling

### Transaction Safety
- **Database Transactions**: Ensures all records created together
- **Rollback**: Failed operations don't create partial records
- **Error Recovery**: Returns empty array on failures

### Logging
- **Detailed Logging**: Entry parameters and processing steps
- **Queue Tracking**: Logs queue message submission
- **Error Context**: Comprehensive error information

### Graceful Degradation
- **Queue Failures**: Notification records still created
- **Database Issues**: Empty response prevents cascade failures
- **User Validation**: Handles invalid user IDs

## Batch Processing

### Multiple Users
- **Array Support**: Single call for multiple recipients
- **Individual Records**: Separate database entries per user
- **Atomic Operation**: All users processed in single transaction

### Performance Optimization
- **Bulk Insert**: Efficient database operations
- **Single Transaction**: Minimizes database overhead
- **Queue Batching**: Individual queue messages per user

## Integration Points

### Used By
- Token notification services
- Transit alert systems
- Weather notification services
- Account management notifications

### External Dependencies
- **Queue Service**: Cloud message delivery
- **MySQL Portal**: Notification storage
- **@maas/core/log**: Comprehensive logging

## Message Features

### Content Support
- **Text Content**: Title and body messaging
- **Rich Media**: Optional image attachments
- **Metadata**: Structured additional information
- **Localization**: Multi-language support

### Delivery Options
- **Silent Notifications**: Background delivery
- **Push Notifications**: Standard user alerts
- **Database Only**: Storage without delivery
- **Image Support**: Visual notification enhancement

## Usage Guidelines

1. **User Arrays**: Always provide users as array for consistency
2. **Language Codes**: Use standard language identifiers
3. **Metadata**: Structure metadata for downstream processing
4. **Error Handling**: Check return values for success confirmation
5. **Queue Health**: Monitor queue delivery for system health

## Security Considerations

- **User Privacy**: No sensitive data in notification content
- **Metadata Security**: Careful handling of additional data
- **Access Control**: Service-level notification permissions
- **Data Retention**: 7-day automatic expiration

## Dependencies

- **@maas/core/mysql**: Database connection management
- **Queue Service**: Cloud messaging infrastructure
- **@maas/core/log**: Centralized logging system
- **Transaction Management**: Database consistency handling