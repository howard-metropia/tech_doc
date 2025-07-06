# RptMailBatch.js - TSP Job Model Documentation

## Quick Summary

The RptMailBatch model manages email report batch processing within the TSP Job scheduling system. This Objection.js ORM model provides database access to the `rpt_mail_batch` table in the portal database, coordinating large-scale email report distribution campaigns. The model is central to the weekly report mailing system that generates personalized transportation reports with trip analytics, weather data, construction alerts, and incentive summaries for MaaS platform users.

## Technical Analysis

### Code Structure
```javascript
const knex = require('@maas/core/mysql')('portal');
class RptMailBatch extends Model {
  static get tableName() {
    return 'rpt_mail_batch';
  }
}
module.exports = RptMailBatch.bindKnex(knex);
```

### Implementation Bug
The model extends the `Model` class without importing it from Objection.js. The correct implementation requires:
```javascript
const { Model } = require('objection');
```

### Database Design
- **Database**: `portal` (MySQL connection via @maas/core)
- **Table**: `rpt_mail_batch`
- **Architecture**: Central coordination table for email batch operations
- **Relationships**: Links to RptMailList and RptMailStatus for complete batch tracking

### Batch Processing Architecture
Based on the reportMail.js service analysis, the model coordinates:
- **Batch Creation**: Unique token generation for each email campaign
- **Status Tracking**: Batch processing state management
- **User Segmentation**: Grouping users for targeted report delivery
- **Performance Monitoring**: Batch completion metrics and timing
- **Error Recovery**: Failed batch retry and recovery mechanisms

## Usage/Integration

### Report Mail Service Integration

**Primary Usage in `src/services/reportMail.js`**:
The model is extensively used in the comprehensive email reporting system that includes:
- **Weekly User Reports**: Personalized transportation analytics and trip summaries
- **Canvas-based Report Generation**: Dynamic visual reports with trip maps and statistics
- **Multi-data Integration**: Weather alerts, construction zones, and incentive information
- **AWS SES Integration**: Large-scale email distribution through Amazon Simple Email Service

### Batch Management Workflow

**Batch Creation Process**:
1. **Token Generation**: Unique batch identifier creation using `genMailBatchToken()`
2. **User List Compilation**: Target user identification and segmentation
3. **Report Template Preparation**: EJS template processing with user-specific data
4. **Batch Queue Management**: Coordinated processing of large email volumes
5. **Status Monitoring**: Real-time batch progress tracking

**Key Integration Points**:
- **Token Management**: 64-character unique token generation for batch identification
- **Collision Prevention**: Database-checked token uniqueness ensuring no duplicates
- **Batch Coordination**: Central control point for multi-step email generation process
- **Performance Tracking**: Batch timing and success rate monitoring

### Scheduling System Integration

**Weekly Report Processing**:
- **Automated Scheduling**: Integration with TSP Job scheduler for regular report delivery
- **Batch Size Management**: Optimal batch sizing to prevent email service limits
- **Resource Management**: Memory and processing resource allocation for large batches
- **Error Handling**: Failed batch recovery and retry logic

**Report Content Coordination**:
- **Trip Analytics**: Weekly trip summaries with mode analysis and distance calculations
- **Weather Integration**: Critical weather alerts and impact on transportation
- **Construction Alerts**: Dynamic construction zone information affecting user routes
- **Incentive Tracking**: Points and rewards summary for user engagement

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql**: Database connection management for portal database
- **objection**: ORM framework (missing import - requires fix)
- **knex**: SQL query builder (provided through @maas/core)

### Related Model Dependencies
- **RptMailList**: Individual email recipient management within batches
- **RptMailStatus**: Email delivery status tracking for each recipient
- **AuthUser**: User profile information for report personalization
- **Trip**: Transportation data for report analytics
- **WeatherCriticalAlert**: Weather data integration for reports
- **ConstructionZone**: Construction alert information for user notifications

### Service Dependencies
- **AWS SDK**: Amazon Web Services integration for email delivery
- **Canvas**: Dynamic report image generation with trip visualizations
- **EJS**: Email template rendering and personalization
- **Moment-timezone**: Date/time processing for report scheduling
- **WebP**: Image compression for optimized email attachments

### External Service Integration
- **Amazon SES**: Large-scale email delivery service
- **InfluxDB**: Performance metrics and batch processing analytics
- **HERE Maps/Google Maps**: Trip visualization and route mapping
- **Font Management**: Custom font loading for report generation

## Code Examples

### Batch Token Generation
```javascript
const RptMailBatch = require('@app/src/models/RptMailBatch');

// Generate unique batch token (from reportMail.js service)
async function genMailBatchToken() {
  let token = genToken(64); // 64-character random token
  let exists = await RptMailBatch.query().where({ token }).first();
  
  while (exists) {
    token = genToken(64);
    exists = await RptMailBatch.query().where({ token }).first();
  }
  
  return token;
}

// Create new email batch
const batchToken = await genMailBatchToken();
const newBatch = await RptMailBatch.query().insert({
  token: batchToken,
  status: 'pending',
  created_at: new Date(),
  user_count: targetUsers.length,
  report_type: 'weekly_summary'
});
```

### Batch Status Management
```javascript
// Update batch processing status
await RptMailBatch.query()
  .findById(batchId)
  .patch({
    status: 'processing',
    started_at: new Date(),
    processed_count: 0
  });

// Complete batch processing
await RptMailBatch.query()
  .findById(batchId)
  .patch({
    status: 'completed',
    completed_at: new Date(),
    processed_count: successfulEmails,
    failed_count: failedEmails,
    processing_time: endTime - startTime
  });
```

### Batch Query and Monitoring
```javascript
// Get active batches
const activeBatches = await RptMailBatch.query()
  .whereIn('status', ['pending', 'processing'])
  .orderBy('created_at', 'desc');

// Get batch processing statistics
const batchStats = await RptMailBatch.query()
  .where('created_at', '>=', startDate)
  .where('created_at', '<', endDate)
  .select(
    knex.raw('COUNT(*) as total_batches'),
    knex.raw('SUM(processed_count) as total_emails'),
    knex.raw('AVG(processing_time) as avg_processing_time'),
    knex.raw('SUM(failed_count) as total_failures')
  )
  .first();
```

### Integration with Email Distribution
```javascript
// Process email batch with report generation
const processEmailBatch = async (batchId) => {
  const batch = await RptMailBatch.query().findById(batchId);
  
  // Get recipient list for this batch
  const recipients = await RptMailList.query()
    .where('batch_token', batch.token)
    .where('status', 'pending');
    
  let processedCount = 0;
  let failedCount = 0;
  
  for (const recipient of recipients) {
    try {
      // Generate personalized report
      const reportData = await generateUserReport(recipient.user_id);
      const reportImage = await createReportCanvas(reportData);
      
      // Send email with AWS SES
      await sendEmailReport(recipient.email, reportImage, reportData);
      
      // Update recipient status
      await RptMailStatus.query()
        .where('mail_list_id', recipient.id)
        .patch({ status: 'sent', sent_at: new Date() });
        
      processedCount++;
    } catch (error) {
      failedCount++;
      logger.error(`Failed to send report to ${recipient.email}: ${error.message}`);
    }
  }
  
  // Update batch completion status
  await RptMailBatch.query()
    .findById(batchId)
    .patch({
      status: 'completed',
      processed_count: processedCount,
      failed_count: failedCount,
      completed_at: new Date()
    });
};
```

### Batch Recovery and Retry Logic
```javascript
// Retry failed batches
const retryFailedBatch = async (batchId) => {
  const failedRecipients = await RptMailList.query()
    .join('rpt_mail_status', 'rpt_mail_list.id', 'rpt_mail_status.mail_list_id')
    .where('rpt_mail_list.batch_token', batchToken)
    .where('rpt_mail_status.status', 'failed');
    
  // Reset failed recipients for retry
  await RptMailStatus.query()
    .whereIn('mail_list_id', failedRecipients.map(r => r.id))
    .patch({ 
      status: 'pending', 
      retry_count: knex.raw('retry_count + 1'),
      last_retry: new Date()
    });
    
  // Update batch for retry processing
  await RptMailBatch.query()
    .findById(batchId)
    .patch({
      status: 'retry',
      retry_started: new Date()
    });
};
```

This model serves as the central coordination point for the sophisticated email reporting system, managing large-scale personalized report distribution while maintaining detailed tracking and recovery capabilities for enterprise-level email campaign management.