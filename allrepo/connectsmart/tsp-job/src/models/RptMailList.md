# RptMailList.js - TSP Job Model Documentation

## Quick Summary

The RptMailList model manages individual email recipients within report batch processing campaigns in the TSP Job scheduling system. This Objection.js ORM model provides database access to the `rpt_mail_list` table in the portal database, maintaining detailed recipient information for large-scale email report distribution. The model works in conjunction with RptMailBatch and RptMailStatus to ensure reliable delivery of personalized transportation reports, weather alerts, and incentive summaries to MaaS platform users.

## Technical Analysis

### Code Structure
```javascript
const knex = require('@maas/core/mysql')('portal');
class RptMailList extends Model {
  static get tableName() {
    return 'rpt_mail_list';
  }
}
module.exports = RptMailList.bindKnex(knex);
```

### Implementation Issue
Similar to other models in the codebase, this model extends the `Model` class without the required import:
```javascript
const { Model } = require('objection');
```

### Database Architecture
- **Database**: `portal` (MySQL connection via @maas/core)
- **Table**: `rpt_mail_list`
- **Role**: Individual recipient management within batch email campaigns
- **Relationships**: Child of RptMailBatch, parent to RptMailStatus tracking

### Recipient Management Design
The model manages detailed recipient information including:
- **User Association**: Links to specific user accounts for personalized reports
- **Email Addresses**: Target email addresses for report delivery
- **Batch Affiliation**: Connection to specific batch campaigns via tokens
- **Personalization Data**: User-specific report customization parameters
- **Delivery Preferences**: Individual user email preferences and settings

## Usage/Integration

### Email Campaign Architecture

**Primary Integration with `src/services/reportMail.js`**:
The model is central to the comprehensive email reporting system that processes:
- **Weekly Transportation Reports**: Personalized trip analytics with visual maps and statistics
- **Weather Alert Integration**: Critical weather notifications affecting user commutes
- **Construction Zone Updates**: Dynamic construction alerts for route planning
- **Incentive Summaries**: Points, rewards, and achievement notifications

### Recipient List Management

**Token-Based Batch Coordination**:
- **Unique Token Generation**: Each recipient receives a unique 64-character token via `genMailListToken()`
- **Batch Association**: Recipients linked to parent batch campaigns through batch tokens
- **Collision Prevention**: Database-validated token uniqueness across all recipients
- **Segmentation Support**: User grouping for targeted report customization

**Recipient Processing Workflow**:
1. **User Identification**: Target user selection based on activity and preferences
2. **Email Validation**: Recipient email address verification and formatting
3. **Token Assignment**: Unique identifier generation for tracking and unsubscribe functionality
4. **Batch Enrollment**: Association with specific email campaign batches
5. **Status Initialization**: Preparation for delivery status tracking

### Report Personalization System

**User-Specific Content Generation**:
- **Trip Analytics**: Individual transportation behavior analysis and insights
- **Route Visualization**: Canvas-generated maps showing user's common routes
- **Weather Integration**: Personalized weather alerts based on user location and travel patterns
- **Incentive Tracking**: Customized points, achievements, and reward summaries
- **Preference-Based Filtering**: Content customization based on user communication preferences

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql**: Database connection management for portal database
- **objection**: ORM framework (missing import - critical bug)
- **knex**: SQL query builder (provided through @maas/core)

### Report Generation Dependencies
- **Canvas API**: Dynamic image generation for personalized trip visualizations
- **EJS Templates**: Email template rendering with user-specific data
- **Moment-timezone**: Date/time processing for report scheduling and formatting
- **AWS SDK**: Amazon SES integration for reliable email delivery
- **WebP Compression**: Optimized image formats for email attachments

### Related Model Dependencies
- **RptMailBatch**: Parent batch coordination and campaign management
- **RptMailStatus**: Delivery status tracking for individual recipients
- **AuthUser**: User profile information for report personalization
- **Trip**: Transportation data for analytics and route visualization
- **WeatherCriticalAlert**: Weather data integration for location-based alerts
- **ConstructionZone**: Construction information for route impact notifications

### Security and Privacy Dependencies
- **Token Management**: Secure unsubscribe and tracking token generation
- **Email Validation**: Recipient address verification and bounce handling
- **Privacy Controls**: User preference management and opt-out functionality
- **Data Protection**: Secure handling of personal information in email content

## Code Examples

### Recipient Token Generation
```javascript
const RptMailList = require('@app/src/models/RptMailList');

// Generate unique recipient token (from reportMail.js service)
async function genMailListToken() {
  let token = genToken(64); // 64-character random token
  let exists = await RptMailList.query().where({ token }).first();
  
  while (exists) {
    token = genToken(64);
    exists = await RptMailList.query().where({ token }).first();
  }
  
  return token;
}

// Add recipient to batch campaign
const recipientToken = await genMailListToken();
const recipient = await RptMailList.query().insert({
  token: recipientToken,
  batch_token: batchToken,
  user_id: userId,
  email: userEmail,
  status: 'pending',
  created_at: new Date(),
  preferences: JSON.stringify(userPreferences)
});
```

### Batch Recipient Management
```javascript
// Get all recipients for a specific batch
const batchRecipients = await RptMailList.query()
  .where('batch_token', batchToken)
  .where('status', 'pending')
  .join('auth_user', 'rpt_mail_list.user_id', 'auth_user.id')
  .select(
    'rpt_mail_list.*',
    'auth_user.first_name',
    'auth_user.last_name',
    'auth_user.timezone'
  );

// Update recipient processing status
await RptMailList.query()
  .where('token', recipientToken)
  .patch({
    status: 'processing',
    processing_started: new Date()
  });
```

### Personalized Report Processing
```javascript
// Process individual recipient with personalized content
const processRecipient = async (recipient) => {
  try {
    // Generate personalized report data
    const reportData = await generateUserReport(recipient.user_id, {
      timeZone: recipient.timezone || 'America/Chicago',
      includeWeather: recipient.preferences?.weather_alerts !== false,
      includeConstruction: recipient.preferences?.construction_alerts !== false,
      reportPeriod: '7days'
    });
    
    // Create visual report with trip maps
    const reportCanvas = await createPersonalizedCanvas(reportData, {
      userId: recipient.user_id,
      userName: `${recipient.first_name} ${recipient.last_name}`,
      tripData: reportData.trips,
      weatherAlerts: reportData.weather,
      constructionZones: reportData.construction
    });
    
    // Generate email content with EJS template
    const emailContent = await ejs.renderFile(
      path.join(__dirname, '../templates/weekly-report.ejs'),
      {
        user: recipient,
        reportData: reportData,
        unsubscribeToken: recipient.token,
        reportImage: reportCanvas.toBuffer('image/png')
      }
    );
    
    return {
      recipient: recipient,
      content: emailContent,
      attachments: [{
        filename: 'weekly-report.png',
        content: reportCanvas.toBuffer('image/png'),
        contentType: 'image/png'
      }]
    };
    
  } catch (error) {
    logger.error(`Failed to process recipient ${recipient.token}: ${error.message}`);
    throw error;
  }
};
```

### Recipient Status Tracking
```javascript
// Query recipients by delivery status
const pendingRecipients = await RptMailList.query()
  .where('batch_token', batchToken)
  .where('status', 'pending')
  .orderBy('created_at', 'asc');

const failedRecipients = await RptMailList.query()
  .where('batch_token', batchToken)
  .where('status', 'failed')
  .where('retry_count', '<', 3); // Limit retry attempts

// Update recipient after successful email delivery
await RptMailList.query()
  .where('token', recipientToken)
  .patch({
    status: 'sent',
    sent_at: new Date(),
    delivery_provider: 'aws-ses',
    message_id: sesMessageId
  });
```

### Unsubscribe and Preference Management
```javascript
// Handle unsubscribe requests using recipient token
const handleUnsubscribe = async (token, unsubscribeType = 'all') => {
  const recipient = await RptMailList.query()
    .where('token', token)
    .first();
    
  if (!recipient) {
    throw new Error('Invalid unsubscribe token');
  }
  
  // Update user preferences
  await AuthUser.query()
    .findById(recipient.user_id)
    .patch({
      email_reports: unsubscribeType !== 'all',
      weather_alerts: unsubscribeType === 'weather' ? false : undefined,
      construction_alerts: unsubscribeType === 'construction' ? false : undefined,
      updated_at: new Date()
    });
    
  // Mark recipient as unsubscribed
  await RptMailList.query()
    .where('token', token)
    .patch({
      status: 'unsubscribed',
      unsubscribed_at: new Date(),
      unsubscribe_type: unsubscribeType
    });
};
```

### Batch Analytics and Reporting
```javascript
// Generate recipient analytics for batch performance
const getBatchAnalytics = async (batchToken) => {
  const analytics = await RptMailList.query()
    .where('batch_token', batchToken)
    .select(
      knex.raw('COUNT(*) as total_recipients'),
      knex.raw('SUM(CASE WHEN status = "sent" THEN 1 ELSE 0 END) as successful_deliveries'),
      knex.raw('SUM(CASE WHEN status = "failed" THEN 1 ELSE 0 END) as failed_deliveries'),
      knex.raw('SUM(CASE WHEN status = "unsubscribed" THEN 1 ELSE 0 END) as unsubscribes'),
      knex.raw('AVG(TIMESTAMPDIFF(SECOND, created_at, sent_at)) as avg_processing_time')
    )
    .first();
    
  return {
    ...analytics,
    delivery_rate: (analytics.successful_deliveries / analytics.total_recipients * 100).toFixed(2),
    failure_rate: (analytics.failed_deliveries / analytics.total_recipients * 100).toFixed(2)
  };
};
```

This model serves as the detailed recipient management layer in the sophisticated email reporting infrastructure, ensuring personalized, trackable, and manageable delivery of transportation analytics and alerts to MaaS platform users while maintaining comprehensive delivery tracking and user preference management.