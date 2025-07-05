# Update Bytemark Tickets Cache Job

## Quick Summary
**Purpose**: Processes ticket refresh requests and sends milestone notifications for users who have earned free METRO tickets through the loyalty program.

**Key Features**:
- Processes ticket purchase and activation refresh logs
- Handles scheduled cache updates
- Sends push notifications for loyalty rewards
- Maintains cache integrity for active users

**Functionality**: Monitors the refresh log table for pending ticket updates, refreshes user caches based on activity types, and delivers notifications for users who've reached the 50-ride milestone to receive 5 free tickets.

## Technical Analysis

### Code Structure
The job handles two main workflows - cache updates and reward notifications:

```javascript
module.exports = {
  inputs: {},
  fn: async () => {
    logger.info(`[update-bytemark-tickets-cache] enter`);
    
    // Ensure cache collection exists
    await service.buildCacheIfEmpty();
    
    // Process cache updates (activity types 1 and 3)
    const logs = await knex('bytemark_ticket_refresh_log')
      .where({ activity_type: 1, status: 0 })
      .orWhere(builder => {
        builder
          .where({ activity_type: 3, status: 0 })
          .andWhere('scheduled_on', '<=', new Date().toISOString());
      })
      .groupBy('user_id')
      .select('user_id');
    
    // Process reward notifications (activity type 2)
    const logs1 = await knex('bytemark_ticket_refresh_log')
      .where({ activity_type: 2, status: 0 })
      .groupBy('user_id')
      .select('user_id');
  },
};
```

### Implementation Details

1. **Activity Type Definitions**:
   - **Type 1**: Immediate cache refresh (ticket purchase/activation)
   - **Type 2**: Loyalty reward notification (50-ride milestone)
   - **Type 3**: Scheduled cache refresh

2. **Cache Update Process**:
   ```javascript
   for (const userId of userIds) {
     try {
       await service.checkTicketCache(userId);
       
       // Mark logs as processed
       await knex('bytemark_ticket_refresh_log')
         .where({ user_id: userId, activity_type: 1, status: 0 })
         .orWhere(builder => {
           builder
             .where({ activity_type: 3, status: 0 })
             .andWhere('scheduled_on', '<=', currentTime);
         })
         .update({ status: 1 });
     } catch (e) {
       logger.warn(`[update-bytemark-tickets-cache] error: ${e.message}`);
     }
   }
   ```

3. **Loyalty Notification Process**:
   ```javascript
   await sendNotification(
     [userId],
     75,  // Notification type for loyalty rewards
     'You've earned 5 free METRO tickets!',
     'As a thank you for taking 50 METRO rides with ConnectSmart, ' +
     'we've added 5 free METRO tickets to your wallet. Way to go!',
     {},
     'en-us',
     false
   );
   ```

### Database Operations

1. **Refresh Log Queries**:
   - Filters unprocessed logs (status = 0)
   - Groups by user to avoid duplicates
   - Checks scheduled_on for future updates

2. **Status Updates**:
   - Sets status = 1 after successful processing
   - Maintains audit trail of processed activities

## Usage/Integration

### Scheduling Configuration
- **Frequency**: Every 5 minutes
- **Timing**: Continuous throughout service hours
- **Priority**: High - affects user experience directly

### Cron Expression
```
*/5 * * * * // Every 5 minutes
```

### Integration Points
1. **MySQL Database**: Refresh log tracking
2. **MongoDB**: Ticket cache storage
3. **Notification Service**: Push notifications
4. **Bytemark Service**: Cache management

## Dependencies

### Required Modules
```javascript
const knex = require('@maas/core/mysql')('portal');
const service = require('@app/src/services/Bytemark');
const { logger } = require('@maas/core/log');
const { sendNotification } = require('@app/src/services/sendNotification');
```

### External Services
1. **MySQL Tables**:
   - `bytemark_ticket_refresh_log`
   - `bytemark_tokens`

2. **MongoDB Collections**:
   - `BytemarkTicketsCache`
   - `BytemarkTicketsLog`

3. **Push Notification Service**:
   - Type 75 notifications
   - Multi-language support

### Configuration Requirements
- Database connections (MySQL and MongoDB)
- Notification service credentials
- Bytemark API configuration
- Logging infrastructure

## Code Examples

### Manual Execution
```javascript
// Run the cache update job manually
const job = require('./update-bytemark-tickets-cache');
await job.fn();
```

### Refresh Log Structure
```javascript
// bytemark_ticket_refresh_log table
{
  id: 1,
  user_id: 'user123',
  activity_type: 1,        // 1=purchase, 2=reward, 3=scheduled
  status: 0,               // 0=pending, 1=processed
  scheduled_on: '2024-01-15 10:00:00',
  created_at: '2024-01-15 09:00:00'
}
```

### Activity Type Processing
```javascript
// Type 1: Immediate refresh after purchase
await knex('bytemark_ticket_refresh_log').insert({
  user_id: userId,
  activity_type: 1,
  status: 0
});

// Type 2: Loyalty reward notification
await knex('bytemark_ticket_refresh_log').insert({
  user_id: userId,
  activity_type: 2,
  status: 0
});

// Type 3: Scheduled refresh
await knex('bytemark_ticket_refresh_log').insert({
  user_id: userId,
  activity_type: 3,
  status: 0,
  scheduled_on: futureDate
});
```

### Notification Payload
```javascript
const notificationData = {
  userIds: [userId],
  notificationType: 75,
  title: 'You've earned 5 free METRO tickets!',
  body: 'As a thank you for taking 50 METRO rides...',
  metadata: {},
  language: 'en-us',
  silent: false
};
```

### Error Handling Patterns
```javascript
// Per-user error isolation
for (const userId of userIds) {
  try {
    await processUser(userId);
  } catch (e) {
    // Log but continue with next user
    logger.warn(`Error processing user ${userId}: ${e.message}`);
  }
}
```

### Performance Optimization

1. **Batch Processing**:
   - Groups logs by user_id
   - Prevents duplicate processing
   - Reduces database queries

2. **Selective Updates**:
   - Only processes pending logs
   - Respects scheduled times
   - Efficient status updates

3. **Cache Initialization**:
   ```javascript
   // Ensures cache exists before processing
   await service.buildCacheIfEmpty();
   ```

### Monitoring Recommendations

1. **Key Metrics**:
   - Cache update success rate
   - Notification delivery rate
   - Processing time per user
   - Error frequency by type

2. **Alerts**:
   - High error rates
   - Notification failures
   - Database connection issues
   - API timeout patterns

3. **Logging Enhancement**:
   ```javascript
   logger.info(`[update-bytemark-tickets-cache] cache update target: ${userIds}`);
   logger.info(`[update-bytemark-tickets-cache] notify users: ${userIds1}`);
   ```

### Business Logic Integration

1. **Loyalty Program**:
   - Triggers at 50 rides
   - Awards 5 free tickets
   - One-time notification per milestone

2. **Real-time Updates**:
   - Immediate cache refresh on purchase
   - Ensures accurate ticket counts
   - Prevents double-spending

3. **User Experience**:
   - Timely notifications
   - Fresh ticket data
   - Seamless reward delivery