# Parking Event Monitoring Test Suite

## Overview
Comprehensive test suite for the parking event monitoring functionality that validates the detection and handling of expired and ongoing ParkMobile parking events. The test verifies the automated processing of parking session status changes, alert notifications, and proper queue task management for real-time monitoring.

## File Location
`/test/testMonitoringParkingEvent.js`

## Technical Analysis

### Core Service Under Test
The test focuses on validating the ParkMobile service functions:
```javascript
const {
  checkExpiredEvents,
  checkOnGoingEvents,
} = require('@app/src/services/parkMobile');
```

These functions handle automated monitoring of parking sessions with different status transitions and alert mechanisms.

### Dependencies
- `@maas/core/bootstrap` - Application bootstrap and configuration
- `chai` - Assertion library with expect interface for test validation
- `sinon` - Mocking framework for stubbing queue operations
- `crypto` - UUID generation for unique transaction identifiers
- `moment` - Date/time manipulation for parking session timing
- `@app/src/models/pmParkingEvent` - Objection.js model for parking events
- `@maas/core/log` - Centralized logging system

### Test Data Architecture

#### Status Constants
```javascript
const status = {
  ON_GOING: 'on-going',
  ALERTED: 'alerted', 
  FINISHED: 'finished'
};
```

#### Mock Event Configuration
The test creates comprehensive mock data representing different parking scenarios:
- **Test User ID**: 1003 (hardcoded test user)
- **Test Zone**: 9994321 (Houston area parking zone)
- **Coordinates**: 29.761104, -95.357932 (specific Houston location)
- **License Plate**: 'fake1234' (mock vehicle identification)

#### Event Scenario Types
1. **Ongoing Event** - Currently active, alert scheduled in 3 minutes
2. **Already Alerted** - Previously alerted, now in alerted status
3. **Just Expired** - Recently finished session requiring status update
4. **Previously Expired** - Already finished, should remain finished
5. **Dummy Event** - Long-duration ongoing session for baseline testing

### Mock Queue Implementation
```javascript
const queue = require('@app/src/services/queue');
const mockQueue = stub(queue, 'sendTask');
mockQueue.callsFake((_, data) => {
  logger.info(data);
  const { id } = data.meta;
  expect(mockEventIds).to.contain(id);
  return true;
});
```

The test stubs the AWS SQS queue service to capture notification tasks without sending actual messages, validating that appropriate events trigger queue operations.

### Database Integration Pattern
```javascript
before(async () => {
  const events = mockEvents.map((event) => mockingEvent(event));
  await Promise.all(
    events.map(async (event) => {
      const res = await PmParkingEvent.query().insert(event);
      mockEventIds.push(res.id);
    }),
  );
});

after(async () => {
  await PmParkingEvent.query().delete().whereIn('id', mockEventIds);
});
```

## Usage/Integration

### Test Execution Flow
1. **Setup Phase**: Creates test parking events with various timing scenarios
2. **Execution Phase**: Calls monitoring functions with current timestamp
3. **Validation Phase**: Verifies correct status transitions and queue notifications
4. **Cleanup Phase**: Removes test data to maintain database integrity

### Key Test Validations
```javascript
it('should pass', async function () {
  const now = moment.utc().toISOString();
  await checkExpiredEvents(now);
  await checkOnGoingEvents(now);

  const expiredEvents = await PmParkingEvent.query().where({
    user_id: testUser,
    zone: testZone,
    status: status.FINISHED,
    alert_before: null,
  });
  expect(expiredEvents.length).to.equal(2);
});
```

The test validates that exactly 2 events transition to 'finished' status, confirming the monitoring logic correctly identifies expired parking sessions.

### Queue Task Verification
The mocked queue function validates that:
- Notification tasks are created for appropriate events
- Task metadata contains correct event IDs
- Queue operations complete successfully without errors

## Code Examples

### UUID Generation Utility
```javascript
const uuid = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = crypto.randomBytes(1)[0] % 16 | 0,
      v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};
```

### Event Mocking Factory
```javascript
const mockingEvent = (options) => {
  const dummyFields = {
    zone: testZone,
    zone_lat: testLat,
    zone_lng: testLng,
    license_plate_number: fakeLpn,
    lpn_country: 'US',
    lpn_state: 'TX',
    park_mobile_transaction_id: uuid(),
  };
  return Object.assign(options, dummyFields);
};
```

### Time-Based Event Creation
```javascript
{
  // ongoing event with alert timing
  user_id: testUser,
  alert_before: 20,
  status: status.ON_GOING,
  alert_at: moment.utc().add(3, 'minutes').toISOString(),
  parking_start_time_UTC: moment.utc().toISOString(),
  parking_stop_time_UTC: moment.utc().add(23, 'minutes').toISOString(),
}
```

## Integration Points

### Service Integration
- **ParkMobile Service**: Core business logic for parking event monitoring
- **Queue Service**: AWS SQS integration for notification delivery
- **Database Model**: Objection.js ORM for parking event persistence

### External Dependencies
- **AWS SQS**: Message queue for asynchronous notification processing
- **MySQL Database**: Persistent storage for parking event records
- **Logging System**: Centralized logging for monitoring and debugging

### Monitoring Workflow
1. **Scheduled Execution**: Job runs periodically to check parking events
2. **Status Detection**: Identifies events requiring status updates
3. **Alert Processing**: Sends notifications for events approaching expiration
4. **Queue Management**: Enqueues notification tasks for delivery
5. **Database Updates**: Updates event status after processing

This test suite ensures the parking event monitoring system correctly handles the complex timing and status management required for real-time parking session tracking and user notifications.