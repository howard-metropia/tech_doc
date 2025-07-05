# ParkMobile Event Monitoring Job Test Suite

## Overview
Comprehensive test suite for the ParkMobile event monitoring background job that validates automated parking session lifecycle management, status transitions, alert notifications, and notification queue integration. This test verifies the complete parking event monitoring workflow from active sessions to expiration handling.

## File Location
`/test/testParkMobileEventMonitoring.js`

## Technical Analysis

### Core Job Function Under Test
```javascript
const { fn: job } = require('@app/src/jobs/parkmobile-event-monitoring');
```

The test validates the main job function that processes parking events and manages their lifecycle states through automated monitoring.

### Dependencies
- `moment` - Date/time manipulation for parking session timing
- `chai` - Assertion library with expect interface for test validation
- `sinon` - Mocking framework for stubbing external services
- `@maas/core/bootstrap` - Application bootstrap and configuration
- `@app/src/models/pmParkingEvent` - Objection.js model for parking events
- `@app/src/models/notification` - Database model for notification records
- `@maas/core/log` - Centralized logging system

### Status Management Architecture

#### Event Status Constants
```javascript
const status = {
  ON_GOING: 'on-going',    // Active parking session
  ALERTED: 'alerted',      // User has been notified
  FINISHED: 'finished',    // Session completed normally
  EXPIRED: 'expired',      // Session expired without completion
};
```

#### Test Configuration Constants
```javascript
const testZone = '987654321';     // Houston parking zone identifier
const fakeLpn = 'MET5566';        // Mock license plate number
const hardcodedArea = 953;        // Geographic area code
const mockUser = 101;             // Test user identifier
```

### Event Creation Factory

#### Dynamic Event Generator
```javascript
const createEvent = (data) => {
  const { status, startTime, endTime, alertBefore } = data;
  const record = {
    user_id: mockUser,
    area: hardcodedArea,
    zone: testZone,
    zone_lat: 29.756498,
    zone_lng: -95.3668,
    parking_start_time_UTC: startTime,
    parking_stop_time_UTC: endTime,
    license_plate_number: fakeLpn,
    lpn_country: 'US',
    lpn_state: 'TX',
    status,
  };
  
  if (alertBefore) {
    record.alert_before = alertBefore;
    record.alert_at = moment
      .utc(endTime)
      .add(alertBefore * -1, 'minute')
      .toISOString();
  }
  return record;
};
```

### Test Scenario Architecture

#### 1. Still Ongoing Event
```javascript
const ongoingEvent = createEvent({
  status: status.ON_GOING,
  startTime: moment.utc().toISOString(),
  endTime: moment.utc().add(45, 'minute').toISOString(),
});
```
Validates that active sessions remain unchanged when not requiring intervention.

#### 2. Should Update to Alerted
```javascript
const alertEvent = createEvent({
  status: status.ON_GOING,
  startTime: moment.utc().add(-40, 'minutes').toISOString(),
  endTime: moment.utc().add(5, 'minute').toISOString(),
  alertBefore: 5,
});
```
Tests automatic alert triggering when approaching expiration time.

#### 3. Still Alerted Event
```javascript
const alertedEvent = createEvent({
  status: status.ALERTED,
  startTime: moment.utc().toISOString(),
  endTime: moment.utc().add(30, 'minutes').toISOString(),
});
```
Ensures already-alerted events maintain their status appropriately.

#### 4. Should Update to Finished
```javascript
const finishEvent = createEvent({
  status: status.ON_GOING,
  startTime: moment.utc().add(-3, 'hours').toISOString(),
  endTime: moment.utc().add(-1, 'minutes').toISOString(),
});
```
Validates proper completion of recently expired sessions.

#### 5. Should Update to Expired
```javascript
const expiredEvent = createEvent({
  status: status.FINISHED,
  startTime: moment.utc().add(-2, 'days').toISOString(),
  endTime: moment.utc().add(-25, 'hours').toISOString(),
});
```
Tests handling of long-expired sessions requiring cleanup.

### Queue Integration Testing

#### AWS SQS Mock Implementation
```javascript
const queue = require('@app/src/services/queue');
const mockQueue = stub(queue, 'sendTask');
await mockQueue.callsFake((_, data) => {
  notifications.push(data.meta);
  shouldNotified = true;
  return true;
});
```

The mock captures notification tasks sent to AWS SQS queue, enabling validation of notification triggering without external service dependencies.

## Usage/Integration

### Test Execution Workflow
1. **Setup Phase**: Creates comprehensive test parking events with various status and timing scenarios
2. **Execution Phase**: Runs the complete parking event monitoring job
3. **Validation Phase**: Verifies correct status transitions and notification queue operations
4. **Cleanup Phase**: Removes test data from both parking events and notification tables

### Status Transition Validation
```javascript
const queryEvents = async (status) => {
  return await PmParkingEvent.query().where({
    user_id: mockUser,
    status,
  });
};

const expiredRecord = await queryEvents(status.EXPIRED);
expect(expiredRecord.length).to.equal(1);

const finishedRecord = await queryEvents(status.FINISHED);
expect(finishedRecord.length).to.equal(1);

const alertedRecord = await queryEvents(status.ALERTED)
expect(alertedRecord.length).to.equal(2);
```

### Notification Queue Verification
```javascript
expect(shouldNotified).to.be.true;
```

Validates that the job successfully triggered notification tasks for appropriate events.

## Code Examples

### Complete Event Lifecycle Test
```javascript
it('should execute successfully and return the expected result', async function () {
  this.timeout(10000);
  let shouldNotified = false;

  // Mock AWS SQS for notification capture
  const queue = require('@app/src/services/queue');
  const mockQueue = stub(queue, 'sendTask');
  await mockQueue.callsFake((_, data) => {
    notifications.push(data.meta);
    shouldNotified = true;
    return true;
  });

  // Execute the complete monitoring job
  await job();

  // Validate all expected status transitions occurred
  const expiredRecord = await queryEvents(status.EXPIRED);
  expect(expiredRecord.length).to.equal(1);
  
  const finishedRecord = await queryEvents(status.FINISHED);
  expect(finishedRecord.length).to.equal(1);
  
  const alertedRecord = await queryEvents(status.ALERTED);
  expect(alertedRecord.length).to.equal(2);

  // Verify notification system activation
  expect(shouldNotified).to.be.true;
});
```

### Geographic Parking Zone Configuration
```javascript
const record = {
  zone_lat: 29.756498,     // Houston downtown area latitude
  zone_lng: -95.3668,      // Houston downtown area longitude
  license_plate_number: fakeLpn,
  lpn_country: 'US',
  lpn_state: 'TX',
};
```

### Alert Timing Calculation
```javascript
if (alertBefore) {
  record.alert_before = alertBefore;
  record.alert_at = moment
    .utc(endTime)
    .add(alertBefore * -1, 'minute')
    .toISOString();
}
```

## Integration Points

### External Service Dependencies
- **AWS SQS**: Message queue for notification delivery
- **ParkMobile API**: Third-party parking service integration
- **Database Systems**: MySQL for parking event persistence
- **Notification Services**: Push notification and email delivery

### Job Scheduling Integration
- **Cron Jobs**: Periodic execution of parking event monitoring
- **Queue Workers**: Processing of notification tasks
- **Database Transactions**: Atomic status updates and record management

### Monitoring and Alerting
- **Event Status Tracking**: Real-time parking session monitoring
- **User Notification System**: Timely alerts for session expiration
- **System Health Monitoring**: Job execution success and failure tracking

### Business Logic Validation
The test ensures proper handling of:
- **Session Lifecycle Management**: Complete parking session state transitions
- **Alert Timing**: Accurate notification scheduling based on user preferences
- **Data Integrity**: Consistent database state after job execution
- **Queue Integration**: Reliable message delivery for notifications

This comprehensive test suite validates the complete ParkMobile event monitoring system, ensuring reliable automated management of parking sessions from initiation through completion or expiration, with appropriate user notifications and system integrations.