# aws_report.js

## Overview
Job module that processes AWS SES (Simple Email Service) event notifications and generates comprehensive email delivery reports. This system transforms SES event data into structured analytics for email campaign monitoring and user engagement tracking.

## Purpose
- Process AWS SES email event notifications for analytics
- Generate detailed email delivery and engagement reports
- Track email campaign performance metrics
- Monitor email deliverability and user interactions

## Key Features
- **Multi-Event Processing**: Handles bounce, delivery, open, click, and complaint events
- **User Resolution**: Maps email addresses to user accounts through multiple methods
- **Duplicate Prevention**: Ensures event data is not processed multiple times
- **Comprehensive Tracking**: Captures all SES event types with detailed metadata
- **Report Aggregation**: Maintains both summary and detailed event records

## Dependencies
```javascript
const moment = require('moment-timezone');
const AuthUsers = require('@app/src/models/AuthUsers');
const SesEvent = require('@app/src/models/SesEvent');
const AwsReports = require('@app/src/models/AwsReports');
const AwsReportDetail = require('@app/src/models/AwsReportDetail');
const { logger } = require('@maas/core/log');
```

## Data Processing Pipeline

### 1. Date Range Configuration
```javascript
const rangeDate = {
  start: moment().subtract(1, 'days').startOf('day').format('YYYY-MM-DD HH:mm:ss'),
  end: moment().subtract(0, 'days').startOf('day').format('YYYY-MM-DD HH:mm:ss'),
};
```

### 2. SES Event Retrieval
```javascript
const sesEventDatas = await SesEvent.find({
  Timestamp: {
    $gte: rangeDate.start,
    $lt: rangeDate.end,
  },
});
```

### 3. Event Processing and Deduplication
```javascript
// Check if notification already processed
const checkNotificationMessageId = await AwsReportDetail.query()
  .where('notification_message_id', sesEventData.MessageId)
  .first();

// Only process valid AWS notifications
if (checkNotificationMessageId === undefined && 
    sesEventData.Subject === 'Amazon SES Email Event Notification') {
  // Process event data
}
```

## User Resolution Strategy

### Method 1: Header-Based User ID
```javascript
const headerId = translateData.mail.headers.findIndex(
  (item) => item.name === 'user_id',
);

if (headerId > -1) {
  userData = {
    id: translateData.mail.headers[headerId].value,
    common_email: translateData.mail.destination[0],
  };
}
```

### Method 2: Email-Based Lookup
```javascript
const getUsersByEmail = async (email) => {
  const getData = await AuthUsers.query()
    .select('id', 'common_email')
    .where('common_email', email)
    .first();
  return getData || null;
};
```

## Event Type Processing

### Supported SES Event Types
- **Bounce**: Email delivery failures and soft/hard bounces
- **Complaint**: Spam complaints and user feedback
- **Delivery**: Successful email delivery confirmations
- **Send**: Email send confirmations from SES
- **Reject**: Email rejections due to policy violations
- **Open**: Email open tracking events
- **Click**: Link click tracking within emails
- **Rendering Failure**: Template rendering errors
- **DeliveryDelay**: Delayed delivery notifications
- **Subscription**: List subscription events

### Event Processing Logic
```javascript
switch (translateData.eventType) {
  case 'Bounce':
    updateArData = { bounce_at: translateData.mail.timestamp };
    otherInfo = translateData.bounce;
    break;
  case 'Delivery':
    updateArData = { delivery_at: translateData.mail.timestamp };
    otherInfo = translateData.delivery;
    break;
  // Additional event types...
}
```

## Database Schema

### AwsReports Table (Summary)
- `report_type`: Classification of email report
- `user_id`: Associated user account
- `user_email`: Recipient email address
- `message_id`: AWS SES message identifier
- `source_email`: Sender email address
- `subject`: Email subject line
- Event timestamp fields (bounce_at, delivery_at, open_at, etc.)

### AwsReportDetail Table (Detailed Events)
- `notification_message_id`: AWS notification identifier
- `report_id`: Reference to summary report
- `event_type`: SES event type
- `message_id`: SES message identifier
- `timestamp`: Event occurrence time
- `from`: Sender address
- `to`: Recipient address
- `subject`: Email subject
- `other_info`: JSON-encoded event metadata

## Report Type Detection
```javascript
let reportType = 0;
const headerId = translateData.mail.headers.findIndex(
  (item) => item.name === 'report_type',
);
if (headerId > -1) {
  reportType = translateData.mail.headers[headerId].value;
}
```

## Performance Optimizations

### Batch Processing
- Processes events in daily batches
- Efficient database queries with indexed lookups
- Memory-efficient iteration over large event sets

### Deduplication Strategy
- Message ID-based duplicate prevention
- Notification ID tracking for event uniqueness
- Efficient existence checks before processing

### User Data Caching
```javascript
let userDatas = {};
if (userDatas[userData.common_email] === undefined) {
  userDatas[userData.common_email] = userData.id;
}
```

## Error Handling and Validation

### Data Validation
- Validates SES notification format and structure
- Ensures required fields are present before processing
- Handles missing or malformed event data gracefully

### Transaction Safety
- Individual event processing isolation
- Proper error logging for debugging
- Continues processing despite individual event failures

## Monitoring and Analytics

### Processing Metrics
```javascript
logger.info(
  `get aws ses email report end at ${moment().toISOString()}, update ${updateCount} aws report record`,
);
```

### Report Analytics
- Email delivery success rates
- User engagement metrics (opens, clicks)
- Bounce and complaint tracking
- Campaign performance analysis

## Integration Points
- **AWS SES**: Email delivery service integration
- **MongoDB**: SES event data storage
- **MySQL**: Report and user data management
- **User Management**: Account resolution and tracking

## Usage Patterns
- Daily scheduled execution for event processing
- Email campaign performance monitoring
- User engagement analytics
- Deliverability issue identification and resolution

## Business Value
- Comprehensive email marketing analytics
- User engagement insights for campaign optimization
- Deliverability monitoring and improvement
- Automated report generation for stakeholder review