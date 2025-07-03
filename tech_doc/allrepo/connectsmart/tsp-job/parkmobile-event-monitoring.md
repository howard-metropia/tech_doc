# ParkMobile Event Monitoring Job

## Quick Summary
**Purpose**: Monitors ParkMobile parking sessions to track expiration times and send timely notifications to users.

**Key Features**:
- Tracks ongoing parking sessions in real-time
- Automatically marks finished and expired parking events
- Sends push notifications before meter expiration
- Processes events at minute-level precision

**Functionality**: Runs periodically to check parking event statuses, update expired sessions, and alert users about upcoming meter expirations through the notification system.

## Technical Analysis

### Code Structure
The job follows a simple modular pattern with two main operations:

```javascript
module.exports = {
  inputs: {},
  fn: async () => {
    const now = moment.utc().startOf('minute').toISOString();
    await checkFinishedAndExpiredEvents(now);
    await checkOnGoingEvents(now);
  },
};
```

### Implementation Details

1. **Time Synchronization**:
   - Uses UTC time with minute-level precision
   - Ensures consistent timing across all operations
   - Prevents race conditions by using `startOf('minute')`

2. **Event Status Management**:
   - Four status levels: `on-going`, `alerted`, `finished`, `expired`
   - Events transition through statuses based on time and notifications
   - Expired events are kept for 24 hours before final expiration

3. **Notification System**:
   - Alerts sent based on user-configured `alert_before` settings
   - Notifications include parking location and remaining time
   - Uses notification type 97 for parking reminders

### Database Operations

**Status Updates**:
```javascript
// Mark events as expired (older than 24 hours)
await PmParkingEvent.query()
  .whereIn('status', [status.ON_GOING, status.ALERTED, status.FINISHED])
  .andWhere('parking_stop_time_UTC', '<=', expiredTime)
  .update({ status: status.EXPIRED });

// Mark events as finished (parking time ended)
await PmParkingEvent.query()
  .whereIn('status', [status.ON_GOING, status.ALERTED])
  .andWhere('parking_stop_time_UTC', '<=', now)
  .update({ status: status.FINISHED });
```

## Usage/Integration

### Scheduling Configuration
- **Frequency**: Every minute (recommended)
- **Timing**: Aligned to minute boundaries for consistency
- **Priority**: High - time-sensitive for user notifications

### Cron Expression
```
* * * * * // Every minute
```

### Integration Points
1. **ParkMobile Service**: Core parking event management
2. **Notification Service**: Push notification delivery
3. **Database Models**: `PmParkingEvent` for event tracking

## Dependencies

### Required Modules
```javascript
const { checkFinishedAndExpiredEvents, checkOnGoingEvents } = require('@app/src/services/parkMobile');
const moment = require('moment/moment');
```

### External Services
1. **ParkMobile API**: For parking session data
2. **Push Notification Service**: For user alerts
3. **MySQL Database**: For event state management

### Configuration Requirements
- ParkMobile vendor configuration
- Notification service credentials
- Database connection settings

## Code Examples

### Manual Execution
```javascript
// Execute the monitoring job manually
const job = require('./parkmobile-event-monitoring');
await job.fn();
```

### Status Transition Flow
```javascript
// Event lifecycle:
// 1. Created with status: 'on-going'
// 2. Alert sent -> status: 'alerted'
// 3. Time expired -> status: 'finished'
// 4. 24 hours later -> status: 'expired'
```

### Notification Payload
```javascript
const notification = {
  userId: event.user_id,
  title: 'Parking Reminder',
  body: `Your meter will expire in ${event.alert_before} minutes.`,
  meta: {
    title: 'Parking Reminder',
    body: `Your meter will expire in ${alert_before} minutes.`,
    id: event.id,
  }
};
```

### Error Handling
The job includes comprehensive error handling:
- Logs all state transitions for audit trails
- Warns on count mismatches between notifications and updates
- Continues processing even if individual notifications fail

### Performance Considerations
- Batch updates for efficiency
- Uses database indexes on status and time fields
- Limits notification processing to 5-minute windows
- Processes multiple events in parallel for notifications

### Monitoring and Logging
```javascript
logger.info(`[park-mobile] ${expiredCount} events expired`);
logger.info(`[park-mobile] ${finishedCount} events finished`);
logger.info(`[park-mobile] ${notifications.length} notifications sent`);
```

The job provides detailed logging for:
- Number of events in each status transition
- Notification delivery confirmations
- Any mismatches in expected vs actual updates