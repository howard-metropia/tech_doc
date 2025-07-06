# AwsReports Model

## Overview
MySQL model for storing AWS SES email campaign reports and delivery analytics.

## File Location
`/src/models/AwsReports.js`

## Database Configuration
- **Connection**: MySQL portal database
- **Table**: `aws_reports`
- **Framework**: Objection.js ORM

## Model Structure
```javascript
class AwsReports extends Model {
  static get tableName() {
    return 'aws_reports';
  }
}
```

## Table Schema
The `aws_reports` table typically contains:

### Primary Fields
- **id**: Primary key identifier
- **report_type**: Type of email report (0=general, custom values)
- **user_id**: Associated user ID
- **user_email**: Recipient email address
- **message_id**: AWS SES message identifier
- **source_email**: Sender email address
- **subject**: Email subject line

### Delivery Status Fields
- **send_at**: Timestamp when email was sent
- **delivery_at**: Timestamp when email was delivered
- **bounce_at**: Timestamp of bounce event
- **complaint_at**: Timestamp of complaint event
- **open_at**: Timestamp when email was opened
- **click_at**: Timestamp when link was clicked
- **reject_at**: Timestamp when email was rejected
- **rendering_failure_at**: Timestamp of rendering failure
- **delivery_delay_at**: Timestamp of delivery delay
- **subscription_at**: Timestamp of subscription event

### Metadata Fields
- **created_at**: Record creation timestamp
- **updated_at**: Record update timestamp

## Usage Context
- **Email Analytics**: Track email campaign performance
- **Delivery Monitoring**: Monitor email deliverability rates
- **User Engagement**: Measure email interaction metrics
- **Compliance**: Handle bounces and complaints

## Integration Points
- AWS SES event processing jobs
- Email campaign analytics dashboards
- User notification systems
- Marketing automation tools

## Related Models
- AwsReportDetail: Detailed event logs
- User models: Email recipients
- Notification systems: Email campaigns

## Performance Considerations
- Indexed on message_id for efficient lookups
- Partitioned by date for large datasets
- Optimized for reporting queries