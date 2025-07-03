# update-user-badge-log-status.js

## Overview
Job module responsible for updating badge progress status in user activity logs by calculating cumulative badge progress across time periods. This job processes badge activity records to maintain accurate running totals of badge progression, handles badge resets when badges are earned, and ensures data consistency in the user achievement tracking system.

## Purpose
- Calculate and update cumulative badge status for user activities
- Handle badge progression tracking across time periods
- Reset accumulated progress when badges are earned
- Maintain data consistency in badge achievement records
- Support analytics and reporting for user engagement metrics

## Key Features
- **Cumulative Progress Tracking**: Maintains running totals of badge progress
- **Earned Badge Handling**: Resets progress counters when badges are completed
- **Multi-Mode Operation**: Supports initial, daily, and custom date processing
- **Data Consistency**: Ensures accurate progression calculations across time periods
- **Efficient Processing**: Optimized database operations for large datasets

## Dependencies
```javascript
const { logger } = require('@maas/core/log');
const moment = require('moment-timezone');
const UserBadgeRelatedActivityLog = require('@app/src/models/UserBadgeRelatedActivityLog');
```

## Core Function Structure
```javascript
module.exports = {
  inputs: { mode: String },
  fn: async function (mode) {
    // Process based on mode: initial, daily, or specific date
    // Calculate cumulative badge progress
    // Update badge status records in database
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
  let startDate = moment('2024-07-05');
  const yesterday = moment().subtract(1, 'days');
  
  while (startDate.isBefore(yesterday) || startDate.isSame(yesterday)) {
    const fetchDate = startDate.format('YYYY-MM-DD');
    const result = await badgeActivityOneDayProcess(fetchDate);
    if (result === 'ERROR') break;
    startDate = startDate.add(1, 'days');
  }
}
```

### Daily Mode
```javascript
if (mode === 'daily') {
  const yesterday = moment().subtract(1, 'days');
  const fetchDate = yesterday.format('YYYY-MM-DD');
  const result = await badgeActivityOneDayProcess(fetchDate);
}
```

### Custom Date Mode
```javascript
else {
  const fetchDate = mode; // Accepts specific date string
  const result = await badgeActivityOneDayProcess(fetchDate);
}
```

## Core Processing Logic

### Main Processing Function
```javascript
const badgeActivityOneDayProcess = async (inputDay) => {
  const zeroDay = moment(inputDay).add(1, 'days');
  const minusOneDay = moment(inputDay);
  const minusTwoDay = moment(inputDay).subtract(1, 'days');
  
  // Get activity records for the target day
  // Build user-badge combination matrix
  // Calculate previous cumulative status
  // Update running totals
  // Apply database updates
};
```

### Data Retrieval
```javascript
const getUserBadgeActivity = async (startDate, endDate) => {
  const resp = await UserBadgeRelatedActivityLog.query()
    .where('activity_datetime', '>', startDate)
    .where('activity_datetime', '<', endDate);
  return resp.length > 0 ? resp : [];
};
```

## Badge Status Calculation

### Previous Status Retrieval
```javascript
const getUserLastBadgeStatus = async (endDate, badgeID, userID) => {
  const resp = await UserBadgeRelatedActivityLog.query()
    .where('activity_datetime', '<', endDate)
    .where('related_badge_id', badgeID)
    .where('user_id', userID)
    .orderBy('id', 'desc')
    .limit(1);
  return resp.length > 0 ? resp : [];
};
```

### Cumulative Status Calculation
```javascript
const getUserAllBadgeStatus = async (data, endDate) => {
  const result = [];
  await Promise.all(data.map(async (d) => {
    const response = await getUserLastBadgeStatus(endDate, d.badgeID, d.userID);
    
    if (response.length > 0) {
      result.push({
        userID: d.userID,
        badgeID: d.badgeID,
        accumulated: response[0].related_badge_status === 'earned badge' 
          ? 0 
          : Number(response[0].related_badge_status)
      });
    } else {
      result.push({
        userID: d.userID,
        badgeID: d.badgeID,
        accumulated: 0
      });
    }
  }));
  return result;
};
```

## Data Processing Algorithm

### User-Badge Matrix Building
```javascript
const userLogs = {};
result.forEach((r) => {
  if (!userLogs[r.user_id]) {
    const badgeList = {};
    badgeList[r.related_badge_id] = true;
    userLogs[r.user_id] = badgeList;
  } else {
    userLogs[r.user_id][r.related_badge_id] = true;
  }
});
```

### Prepared List Generation
```javascript
const preparedList = [];
for (const uID in userLogs) {
  if (userLogs[uID]) {
    for (const bID in userLogs[uID]) {
      if (userLogs[uID][bID]) {
        preparedList.push({ userID: uID, badgeID: bID });
      }
    }
  }
}
```

### Running Total Calculation
```javascript
result.forEach((r) => {
  if (r.related_badge_status === 'earned badge') {
    finalUserLogs[r.user_id][r.related_badge_id] = 0;
  } else {
    finalUserLogs[r.user_id][r.related_badge_id] = 
      Number(r.related_badge_status) + finalUserLogs[r.user_id][r.related_badge_id];
    
    finalUpdateList.push({
      id: r.id,
      status: finalUserLogs[r.user_id][r.related_badge_id]
    });
  }
});
```

## Database Update Operations

### Record Update Function
```javascript
const updateBadgeActivityRecord = async (data) => {
  for (const r of data) {
    const result = await UserBadgeRelatedActivityLog.query()
      .findById(r.id)
      .patch({ related_badge_status: `${r.status}` });
    
    if (!result) {
      logger.info(`[update-user-badge-log-status][updateBadgeActivityRecord] error on id: ${r.id}`);
      return 'ERROR';
    }
  }
  return 'OK';
};
```

### Batch Update Processing
- Processes all updates for a single day in sequence
- Maintains data consistency through individual record updates
- Provides error tracking for failed update operations

## Badge Status Logic

### Earned Badge Handling
- When a badge is earned (`related_badge_status === 'earned badge'`):
  - Reset accumulated count to 0
  - No database update needed (status already correct)
  - Subsequent activities start fresh count

### Progress Accumulation
- For non-earned badges:
  - Add current activity progress to previous accumulated total
  - Update database record with new cumulative status
  - Maintain running total for next activity

## Error Handling Strategy

### Database Error Management
```javascript
try {
  // Database operations
} catch (e) {
  logger.error(`[update-user-badge-log-status][function] error: ${e.message}`);
  logger.info(`[update-user-badge-log-status][function] stack: ${e.stack}`);
  return 'ERROR';
}
```

### Processing Error Recovery
- Early termination on database errors
- Comprehensive error logging with context
- Graceful degradation for individual record failures

## Performance Optimization

### Efficient Query Patterns
- Time-based filtering to minimize data processing
- Indexed queries on activity_datetime field
- Optimized sort and limit operations

### Memory Management
- Single-day processing to control memory usage
- Efficient data structures for user-badge mapping
- Minimal object creation during processing

## Logging and Monitoring

### Process Tracking
```javascript
logger.info(`[update-user-badge-log-status][badgeActivityOneDayProcess] update ${finalUpdateList.length} records for ${inputDay} done`);
logger.info(`[update-user-badge-log-status][badgeActivityOneDayProcess] dealing with ${inputDay} done with no data`);
```

### Error Logging
```javascript
logger.error(`[update-user-badge-log-status] initial mode error!`);
logger.error(`[update-user-badge-log-status] error: ${e.message}`);
```

## Data Consistency Features

### Temporal Accuracy
- Processes activities in chronological order
- Maintains accurate cumulative totals across time periods
- Handles date boundaries correctly

### Badge State Management
- Properly resets counters when badges are earned
- Maintains separate progression tracking per user-badge combination
- Ensures data integrity during batch processing

## Use Cases

### Historical Data Processing
- Initial setup for cumulative status calculation
- Bulk processing of existing activity records
- Data migration and system initialization

### Daily Status Updates
- Regular daily maintenance of badge progression
- Maintains current state of user achievements
- Supports real-time analytics and dashboards

### Data Recovery Processing
- On-demand processing for specific dates
- Correction of data inconsistencies
- Development and testing support

## Integration Points

### Internal Systems
- **UserBadgeRelatedActivityLog Model**: Primary data source and target
- **Badge System**: User achievement progression tracking
- **Analytics Systems**: User engagement metrics and reporting
- **Dashboard Systems**: Real-time achievement status display

## Security Considerations
- Database access control and authentication
- Data integrity protection during updates
- Audit trails for status modifications
- Error handling to prevent data corruption

## Deployment Notes
- Requires database write permissions
- Dependent on UserBadgeRelatedActivityLog table structure
- Memory considerations for large datasets
- Proper error handling for production stability

## Future Enhancements
- Parallel processing for improved performance
- Advanced error recovery and retry mechanisms
- Real-time status calculation capabilities
- Enhanced monitoring and alerting
- Support for complex badge progression rules
- Optimized batch update operations