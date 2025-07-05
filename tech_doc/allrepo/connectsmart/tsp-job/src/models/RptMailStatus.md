# RptMailStatus.js - TSP Job Model Documentation

## Quick Summary

The RptMailStatus model tracks detailed email delivery status and performance metrics within the TSP Job email reporting system. This Objection.js ORM model provides database access to the `rpt_mail_status` table in the portal database, maintaining comprehensive delivery tracking for individual email recipients across batch campaigns. The model serves as the final tracking layer in the three-tier email system (RptMailBatch → RptMailList → RptMailStatus), providing granular delivery confirmation, bounce handling, and retry management for enterprise-scale email operations.

## Technical Analysis

### Code Structure
```javascript
const knex = require('@maas/core/mysql')('portal');
class RptMailStatus extends Model {
  static get tableName() {
    return 'rpt_mail_status';
  }
}
module.exports = RptMailStatus.bindKnex(knex);
```

### Implementation Bug
Consistent with other models in the codebase, this model extends the `Model` class without importing it:
```javascript
const { Model } = require('objection');
```

### Database Design
- **Database**: `portal` (MySQL connection via @maas/core)
- **Table**: `rpt_mail_status`
- **Architecture**: Granular delivery status tracking for each email recipient
- **Relationship**: Child of RptMailList, providing detailed status for individual email deliveries

### Status Tracking Architecture
The model maintains comprehensive delivery information including:
- **Delivery Confirmation**: Successful email delivery timestamps and provider confirmation
- **Bounce Management**: Failed delivery tracking with categorized failure reasons
- **Retry Logic**: Automated retry attempts with exponential backoff and failure limits
- **Provider Integration**: AWS SES message IDs and delivery receipt processing
- **Performance Metrics**: Delivery timing, processing duration, and success rates

## Usage/Integration

### Email Delivery Pipeline Integration

**Core Role in `src/services/reportMail.js`**:
The model provides the final status tracking layer for the comprehensive email reporting system that includes:
- **Personalized Weekly Reports**: Transportation analytics with visual trip maps and statistics
- **Real-time Weather Alerts**: Critical weather notifications based on user location and travel patterns
- **Construction Zone Updates**: Dynamic construction alerts affecting user commute routes
- **Incentive Notifications**: Points, rewards, and achievement summaries for user engagement

### Delivery Status Management

**Status Lifecycle Tracking**:
1. **Initial Status**: Created when recipient is added to email queue ('pending')
2. **Processing State**: Updated when email generation begins ('processing')
3. **Delivery Attempt**: Marked during actual email transmission ('sending')
4. **Success Confirmation**: Confirmed delivery with provider message ID ('delivered')
5. **Failure Handling**: Failed delivery with categorized error information ('failed')
6. **Retry Management**: Automated retry attempts with failure reason tracking

**AWS SES Integration**:
- **Message ID Tracking**: Storage of AWS SES message identifiers for delivery confirmation
- **Bounce Handling**: Processing of bounce notifications and categorization
- **Complaint Management**: Handling of spam complaints and unsubscribe requests
- **Delivery Receipts**: Processing of delivery confirmation webhooks

### Performance Monitoring and Analytics

**Delivery Metrics Collection**:
- **Processing Time**: Duration from email generation to delivery attempt
- **Delivery Latency**: Time between send attempt and delivery confirmation
- **Retry Analysis**: Success rates of retry attempts and optimal retry intervals
- **Provider Performance**: AWS SES delivery performance and error rate tracking
- **Batch Success Rates**: Aggregate delivery performance across email campaigns

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql**: Database connection management for portal database
- **objection**: ORM framework (missing import - critical bug requiring fix)
- **knex**: SQL query builder (provided through @maas/core)

### Email Service Dependencies
- **AWS SDK**: Amazon Simple Email Service integration for enterprise email delivery
- **SES Webhooks**: Delivery confirmation and bounce notification processing
- **Email Validation**: Recipient address verification and formatting
- **Rate Limiting**: AWS SES sending rate management and throttling

### Related Model Dependencies
- **RptMailList**: Parent recipient information and batch association
- **RptMailBatch**: Campaign-level batch coordination and management
- **AuthUser**: User profile information for personalization and preferences
- **Email Templates**: EJS template system for dynamic content generation

### Monitoring and Alerting Dependencies
- **InfluxDB**: Performance metrics and delivery analytics storage
- **Logger**: Comprehensive error logging and delivery event tracking
- **Alert Systems**: Failed delivery notifications and system health monitoring
- **Dashboard Integration**: Real-time delivery status monitoring and reporting

## Code Examples

### Status Initialization and Tracking
```javascript
const RptMailStatus = require('@app/src/models/RptMailStatus');

// Initialize status record for new email
const initializeEmailStatus = async (mailListId, recipientEmail) => {
  return await RptMailStatus.query().insert({
    mail_list_id: mailListId,
    recipient_email: recipientEmail,
    status: 'pending',
    created_at: new Date(),
    retry_count: 0,
    last_attempt: null,
    provider: 'aws-ses'
  });
};

// Update status during email processing
await RptMailStatus.query()
  .where('mail_list_id', recipientId)
  .patch({
    status: 'processing',
    processing_started: new Date(),
    last_attempt: new Date()
  });
```

### Delivery Confirmation Processing
```javascript
// Handle successful email delivery
const confirmDelivery = async (messageId, deliveryTimestamp) => {
  const status = await RptMailStatus.query()
    .where('message_id', messageId)
    .first();
    
  if (status) {
    await RptMailStatus.query()
      .findById(status.id)
      .patch({
        status: 'delivered',
        delivered_at: new Date(deliveryTimestamp),
        delivery_confirmed: true,
        processing_time: new Date() - new Date(status.processing_started)
      });
      
    logger.info(`Email delivery confirmed for message ${messageId}`);
  }
};

// Process AWS SES delivery notification
const processSESDeliveryNotification = async (sesNotification) => {
  const { messageId, delivery } = sesNotification;
  
  await confirmDelivery(messageId, delivery.timestamp);
  
  // Update delivery metrics
  await RptMailStatus.query()
    .where('message_id', messageId)
    .patch({
      delivery_delay: delivery.processingTimeMillis,
      smtp_response: delivery.smtpResponse,
      reporting_mta: delivery.reportingMTA
    });
};
```

### Bounce and Failure Handling
```javascript
// Handle email bounce notifications
const processBounce = async (messageId, bounceDetails) => {
  const bounceType = bounceDetails.bounceType; // 'Permanent' or 'Transient'
  const bounceSubType = bounceDetails.bounceSubType;
  
  await RptMailStatus.query()
    .where('message_id', messageId)
    .patch({
      status: bounceType === 'Permanent' ? 'permanently_failed' : 'temporarily_failed',
      bounce_type: bounceType,
      bounce_subtype: bounceSubType,
      bounce_reason: bounceDetails.bouncedRecipients[0]?.diagnosticCode,
      bounced_at: new Date(bounceDetails.timestamp),
      retry_eligible: bounceType === 'Transient'
    });
    
  // If permanent bounce, update recipient preferences
  if (bounceType === 'Permanent') {
    const statusRecord = await RptMailStatus.query()
      .where('message_id', messageId)
      .join('rpt_mail_list', 'rpt_mail_status.mail_list_id', 'rpt_mail_list.id')
      .first();
      
    if (statusRecord) {
      await AuthUser.query()
        .findById(statusRecord.user_id)
        .patch({
          email_reports: false,
          bounce_reason: bounceSubType,
          last_bounce: new Date()
        });
    }
  }
};
```

### Retry Management System
```javascript
// Process failed emails for retry
const processRetries = async () => {
  const retryableFailures = await RptMailStatus.query()
    .where('status', 'temporarily_failed')
    .where('retry_count', '<', 3)
    .where('retry_eligible', true)
    .where('next_retry', '<=', new Date())
    .join('rpt_mail_list', 'rpt_mail_status.mail_list_id', 'rpt_mail_list.id');
    
  for (const failure of retryableFailures) {
    try {
      // Calculate exponential backoff delay
      const retryDelay = Math.pow(2, failure.retry_count) * 3600000; // Hours in milliseconds
      
      // Update retry attempt
      await RptMailStatus.query()
        .findById(failure.id)
        .patch({
          status: 'retrying',
          retry_count: failure.retry_count + 1,
          last_retry: new Date(),
          next_retry: new Date(Date.now() + retryDelay)
        });
        
      // Attempt email resend
      const emailResult = await resendEmail(failure);
      
      if (emailResult.success) {
        await RptMailStatus.query()
          .findById(failure.id)
          .patch({
            status: 'sent',
            message_id: emailResult.messageId,
            sent_at: new Date(),
            retry_successful: true
          });
      } else {
        await RptMailStatus.query()
          .findById(failure.id)
          .patch({
            status: 'temporarily_failed',
            last_error: emailResult.error,
            error_count: knex.raw('error_count + 1')
          });
      }
      
    } catch (error) {
      logger.error(`Retry failed for status ${failure.id}: ${error.message}`);
    }
  }
};
```

### Analytics and Performance Reporting
```javascript
// Generate delivery performance analytics
const getDeliveryAnalytics = async (batchToken, dateRange) => {
  const analytics = await RptMailStatus.query()
    .join('rpt_mail_list', 'rpt_mail_status.mail_list_id', 'rpt_mail_list.id')
    .where('rpt_mail_list.batch_token', batchToken)
    .where('rpt_mail_status.created_at', '>=', dateRange.start)
    .where('rpt_mail_status.created_at', '<=', dateRange.end)
    .select(
      knex.raw('COUNT(*) as total_emails'),
      knex.raw('SUM(CASE WHEN status = "delivered" THEN 1 ELSE 0 END) as delivered_count'),
      knex.raw('SUM(CASE WHEN status = "permanently_failed" THEN 1 ELSE 0 END) as permanent_failures'),
      knex.raw('SUM(CASE WHEN status = "temporarily_failed" THEN 1 ELSE 0 END) as temporary_failures'),
      knex.raw('SUM(retry_count) as total_retries'),
      knex.raw('AVG(processing_time) as avg_processing_time'),
      knex.raw('AVG(delivery_delay) as avg_delivery_delay')
    )
    .first();
    
  return {
    ...analytics,
    delivery_rate: (analytics.delivered_count / analytics.total_emails * 100).toFixed(2),
    failure_rate: ((analytics.permanent_failures + analytics.temporary_failures) / analytics.total_emails * 100).toFixed(2),
    retry_success_rate: analytics.total_retries > 0 ? 
      (analytics.delivered_count / (analytics.total_emails + analytics.total_retries) * 100).toFixed(2) : 0
  };
};

// Monitor real-time delivery status
const getDeliveryStatus = async (batchToken) => {
  return await RptMailStatus.query()
    .join('rpt_mail_list', 'rpt_mail_status.mail_list_id', 'rpt_mail_list.id')
    .where('rpt_mail_list.batch_token', batchToken)
    .select(
      'rpt_mail_status.status',
      knex.raw('COUNT(*) as count')
    )
    .groupBy('rpt_mail_status.status')
    .orderBy('count', 'desc');
};
```

### Integration with Health Monitoring
```javascript
// System health check for email delivery service
const checkEmailDeliveryHealth = async () => {
  const recentFailures = await RptMailStatus.query()
    .where('created_at', '>=', new Date(Date.now() - 3600000)) // Last hour
    .where('status', 'permanently_failed')
    .count('* as failure_count')
    .first();
    
  const recentDeliveries = await RptMailStatus.query()
    .where('created_at', '>=', new Date(Date.now() - 3600000))
    .count('* as total_count')
    .first();
    
  const failureRate = recentDeliveries.total_count > 0 ? 
    (recentFailures.failure_count / recentDeliveries.total_count) : 0;
    
  if (failureRate > 0.1) { // 10% failure rate threshold
    logger.warn(`High email failure rate detected: ${(failureRate * 100).toFixed(2)}%`);
    // Trigger alert to operations team
  }
  
  return {
    healthy: failureRate < 0.05,
    failure_rate: failureRate,
    recent_failures: recentFailures.failure_count,
    recent_total: recentDeliveries.total_count
  };
};
```

This model provides the critical final layer of email delivery tracking, ensuring reliable, monitorable, and recoverable email operations for the comprehensive MaaS platform communication system while maintaining detailed analytics and automated recovery capabilities for enterprise-scale email delivery management.