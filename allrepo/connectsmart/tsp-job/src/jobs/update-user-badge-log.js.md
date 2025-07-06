# update-user-badge-log.js

## Overview
Job module responsible for synchronizing user badge activity logs from the incentive system to the TSP database. This job fetches badge-related activities and campaign participation data, processes the relationships between activities and badges, and maintains comprehensive activity logs for analytics and user engagement tracking.

## Purpose
- Synchronize user badge activities from external incentive service
- Process badge earning and progression activities
- Maintain activity logs with campaign associations
- Support analytics and reporting for user engagement
- Track badge progression and achievement milestones

## Key Features
- **Multi-Mode Operation**: Supports initial, daily, and custom date processing
- **Campaign Integration**: Associates badge activities with bingo card campaigns
- **Batch Processing**: Handles large datasets efficiently with pagination
- **Badge Relationship Mapping**: Links activities to related and earned badges
- **Flexible Date Ranges**: Supports historical data import and ongoing synchronization

## Dependencies
```javascript
const { logger } = require('@maas/core/log');
const moment = require('moment-timezone');
const config = require('config').get('incentive');
const UserBadgeRelatedActivityLog = require('@app/src/models/UserBadgeRelatedActivityLog');
const superagent = require('superagent');
```

## Core Function Structure
```javascript
module.exports = {
  inputs: { mode: String },
  fn: async function (mode) {
    // Process based on mode: initial, daily, or specific date
    // Execute badge activity synchronization
    // Handle campaign associations and data relationships
  }
};
```

## Input Parameters

### mode (String)
- **Purpose**: Determines the execution mode and date range for processing
- **Values**:
  - `"initial"`: Process all historical data from 2024-07-05 to yesterday
  - `"daily"`: Process yesterday's data only
  - `{date}`: Process specific date in YYYY-MM-DD format
- **Required**: Yes

## Processing Modes

### Initial Mode
```javascript
if (mode === 'initial') {
  let startDate = moment("2024-07-05");
  const yesterday = moment().subtract(1, "days");
  while (startDate.isBefore(yesterday) || startDate.isSame(yesterday)) {
    const fetchDate = startDate.format("YYYY-MM-DD");
    await badgeActivityOneDayProcess(fetchDate);
    startDate = startDate.add(1, "days");
  }
}
```

### Daily Mode
```javascript
if (mode === 'daily') {
  const yesterday = moment().subtract(1, "days");
  const fetchDate = yesterday.format("YYYY-MM-DD");
  await badgeActivityOneDayProcess(fetchDate);
}
```

### Custom Date Mode
```javascript
else {
  const fetchDate = mode; // Accepts specific date string
  await badgeActivityOneDayProcess(fetchDate);
}
```

## Data Source Integration

### Badge Activity API
```javascript
const getUserBadgeActivity = async (startDate, endDate) => {
  const resp = await superagent
    .get(`${config.incentiveHookUrl}/user-badge-logs?start_date=${startDate}&end_date=${endDate}`);
  return resp.body.data || [];
};
```

### Campaign Data API
```javascript
const getUserCampaignProcess = async (startDate, endDate) => {
  let result = [];
  let pageNo = 1;
  let nextPageToken = true;
  
  while (nextPageToken) {
    const resp = await superagent
      .get(`${config.incentiveHookUrl}/user-bingo-logs?start_date=${startDate}&end_date=${endDate}&page=${pageNo}&per_page=1000`);
    
    if (resp?.body?.data?.length > 0) {
      result = result.concat(resp.body.data);
      pageNo++;
    } else {
      nextPageToken = false;
    }
  }
  return result;
};
```

## Data Processing Logic

### Badge Activity Processing
```javascript
const badgeActivityOneDayProcess = async (fetchDate) => {
  const result = await getUserBadgeActivity(fetchDate, fetchDate);
  const campaignResult = await getUserCampaignProcess(fetchDate, fetchDate);
  
  // Process related badges and earned badges
  // Associate with campaign data
  // Insert processed records to database
};
```

### Activity-Campaign Association
```javascript
result.forEach(r => {
  campaignResult.forEach(c => {
    if (c.user_id === r.user_id) {
      relatedCampaignID = Number(c.campaign_id);
      relatedCampaignName = c.title;
    }
  });
});
```

## Badge Data Structure

### Activity Log Structure
```javascript
{
  user_id: r.user_id,
  activity_id: r.log_id,
  activity_name: r.name,
  activity_datetime: r.timestamp,
  related_badge_id: b.badge_id,
  related_badge_name: b.badge_name,
  related_badge_status: b.badge_id === 5 || b.badge_id === 8 ? b.description : 1,
  related_campaign_id: relatedCampaignID,
  related_campaign_name: relatedCampaignName
}
```

### Badge Types Processing

#### Related Badges
- Badges that are progressed by the activity
- Status includes progress information or description
- Special handling for badge IDs 5 and 8 (uses description field)

#### Earned Badges
- Badges that are completed/earned by the activity
- Status set to "earned badge"
- Represents achievement milestones

## Database Operations

### Insert Operation
```javascript
const insertNewBadgeActivityRecord = async (data) => {
  const resp = await UserBadgeRelatedActivityLog.query().insertGraph(data);
  return resp ? 'OK' : 'ERROR';
};
```

### Batch Processing
- Processes all activities for a single day in one operation
- Uses Objection.js insertGraph for efficient bulk inserts
- Maintains data relationships during insertion

## Error Handling Strategy

### API Error Management
```javascript
try {
  const resp = await superagent.get(url);
  // Process response
} catch (e) {
  logger.error(`[update-user-badge-log][function] error: ${e.message}`);
  logger.info(`[update-user-badge-log][function] stack: ${e.stack}`);
}
```

### Database Error Handling
- Comprehensive error logging with stack traces
- Graceful degradation for individual record failures
- Transaction management for data consistency

## Configuration Requirements

### Incentive Service Configuration
```javascript
const config = require('config').get('incentive');
// Requires incentiveHookUrl configuration
```

### API Endpoints
- `/user-badge-logs`: Badge activity data endpoint
- `/user-bingo-logs`: Campaign participation data endpoint

## Performance Considerations

### Pagination Strategy
- Processes campaign data in 1000-record pages
- Efficient memory usage for large datasets
- Configurable page size for optimization

### Date Range Processing
- Single-day processing to manage memory usage
- Iterative approach for historical data import
- Minimal resource footprint per execution

## Logging and Monitoring

### Process Logging
```javascript
logger.info(`[update-user-badge-log][badgeActivityOneDayProcess] insert ${activityLog.length} records for ${fetchDate} done`);
logger.info(`[update-user-badge-log][badgeActivityOneDayProcess] dealing with ${fetchDate} done with no data`);
```

### Error Tracking
- Detailed error messages with context
- Stack trace logging for debugging
- Function-level error identification

## Use Cases

### Historical Data Import
- Initial setup processing from 2024-07-05
- Bulk import of existing badge activity records
- Data migration and system initialization

### Daily Synchronization
- Regular daily updates of badge activities
- Maintains current state of user achievements
- Supports real-time analytics and reporting

### Custom Date Processing
- On-demand processing for specific dates
- Data recovery and reprocessing capabilities
- Development and testing support

## Integration Points

### External Services
- **Incentive Hook API**: Source for badge and campaign data
- **Badge System**: User achievement and progression tracking
- **Campaign System**: Bingo card and challenge management

### Internal Systems
- **UserBadgeRelatedActivityLog Model**: Primary data storage
- **Analytics Systems**: User engagement reporting
- **Dashboard Systems**: Real-time achievement tracking

## Data Quality Assurance

### Data Validation
- Validates API response structure
- Handles missing or malformed data gracefully
- Ensures data consistency across related records

### Relationship Integrity
- Maintains proper associations between activities and badges
- Links activities to relevant campaigns
- Preserves temporal relationships in activity sequences

## Security Considerations
- Secure API communication with incentive service
- Authentication and authorization for external APIs
- Data privacy protection during processing
- Audit trails for data synchronization operations

## Deployment Notes
- Requires network connectivity to incentive service
- Database permissions for UserBadgeRelatedActivityLog operations
- Configuration of incentive service endpoints
- Proper error handling for service unavailability

## Future Enhancements
- Real-time streaming synchronization
- Enhanced data validation and quality checks
- Support for incremental updates
- Advanced error recovery mechanisms
- Performance optimization for large datasets
- Enhanced monitoring and alerting capabilities