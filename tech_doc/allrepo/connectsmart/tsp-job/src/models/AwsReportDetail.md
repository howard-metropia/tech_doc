# AwsReportDetail Model

## Overview
MySQL model for storing detailed AWS SES email event logs and granular tracking information.

## File Location
`/src/models/AwsReportDetail.js`

## Database Configuration
- **Connection**: MySQL portal database
- **Table**: `aws_report_detail`
- **Framework**: Objection.js ORM

## Model Structure
```javascript
class AwsReportDetail extends Model {
  static get tableName() {
    return 'aws_report_detail';
  }
}
```

## Table Schema
The `aws_report_detail` table provides granular event tracking:

### Primary Fields
- **id**: Primary key identifier
- **notification_message_id**: AWS SNS notification message ID
- **report_id**: Foreign key to aws_reports table
- **event_type**: Type of email event (Send, Delivery, Bounce, etc.)
- **message_id**: AWS SES message identifier
- **timestamp**: Event occurrence timestamp

### Email Details
- **from**: Sender email address
- **to**: Recipient email address
- **subject**: Email subject line
- **other_info**: JSON field with additional event data

### Audit Fields
- **created_at**: Record creation timestamp
- **updated_at**: Record update timestamp

## Event Types
Supported AWS SES event types:
- **Send**: Email sent from SES
- **Delivery**: Email delivered to recipient
- **Bounce**: Email bounced back
- **Complaint**: Recipient marked as spam
- **Open**: Recipient opened email
- **Click**: Recipient clicked link
- **Reject**: Email rejected by SES
- **Rendering Failure**: Email rendering failed
- **DeliveryDelay**: Email delivery delayed
- **Subscription**: Subscription management event

## Other Info JSON Structure
The `other_info` field stores event-specific data:

### Bounce Events
```json
{
  "bounceType": "Permanent",
  "bounceSubType": "General",
  "bouncedRecipients": [...]
}
```

### Complaint Events
```json
{
  "complaintFeedbackType": "abuse",
  "complainedRecipients": [...]
}
```

### Click Events
```json
{
  "link": "https://example.com",
  "linkTags": {...}
}
```

## Relationships
- **Parent**: Links to AwsReports via report_id
- **Event Chain**: Multiple detail records per report
- **Deduplication**: Prevents duplicate event processing

## Usage Context
- **Detailed Analytics**: Granular email event analysis
- **Debugging**: Troubleshoot email delivery issues
- **Compliance**: Track bounces and complaints
- **User Behavior**: Analyze email engagement patterns

## Performance Considerations
- Indexed on notification_message_id for deduplication
- Indexed on report_id for relationship queries
- JSON field optimized for event-specific queries
- Partitioned by timestamp for historical data

## Related Components
- AWS SES event processing pipeline
- Email analytics dashboards
- Bounce and complaint handling systems
- Email deliverability monitoring