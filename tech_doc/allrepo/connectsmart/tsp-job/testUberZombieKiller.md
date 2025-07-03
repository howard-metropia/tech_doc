# TSP Job Test: Uber Zombie Killer Process Integration Test Documentation

## Quick Summary

**Purpose**: Comprehensive integration test suite for the Uber "zombie killer" service that identifies and updates stale trip records by synchronizing with real-time Uber API status updates.

**Key Features**:
- Tests `processZombieTrips()` service for stale trip detection and updates
- Validates trip status transitions across multiple Uber states
- Handles status changes from processing → in_progress → completed/canceled
- Tests notification delivery for status changes
- Validates trip termination and telework log updates
- Includes incentive reward testing for completed trips

**Technology Stack**: Mocha testing framework, Chai assertions, Nock for HTTP mocking, UUID generation, Moment.js for dates

## Technical Analysis

### Code Structure

The test file implements a comprehensive testing framework for zombie trip detection and status synchronization:

```javascript
// Core testing dependencies
const expect = require('chai').expect;
require('@maas/core/bootstrap');

// HTTP mocking and utilities
const nock = require('nock');
const moment = require('moment-timezone');
const { v4: uuidv4 } = require('uuid');

// Database models for complete trip lifecycle
const Trips = require('@app/src/models/Trips');
const Teleworks = require('@app/src/models/Teleworks');
const TeleworkLogs = require('@app/src/models/TeleworkLogs');
const RidehailTrips = require('@app/src/models/RidehailTrips');
const Notifications = require('@app/src/models/Notifications');
const AuthUsers = require('@app/src/models/AuthUsers');
const IncentiveNotifyQueue = require('@app/src/models/IncentiveNotifyQueue');

// Uber service integration
const uberServices = require('@app/src/services/uber/guest-ride');
```

### Key Components

**Zombie Trip Detection Logic**:
- Identifies trips with outdated status information (created >35 minutes ago)
- Queries Uber API for current trip status
- Updates local database with real-time status information
- Triggers appropriate notifications and business logic

**Status Transition Testing**:
The test covers comprehensive status transition scenarios:

```javascript
// Primary status transitions tested
processing → in_progress
processing → completed  
processing → driver_canceled
processing → driver_redispatched

accepted → in_progress
accepted → completed
accepted → driver_canceled
accepted → driver_redispatched

arriving → in_progress
arriving → completed
arriving → driver_canceled
arriving → driver_redispatched

in_progress → completed
driver_redispatched → accepted
driver_redispatched → in_progress
```

**Mock Data Architecture**:
```javascript
const mockRidehailTrip = {
  // ... standard trip data
  created_at: moment.utc().add(-35, 'minutes').toISOString(),
  updated_at: moment.utc().add(-35, 'minutes').toISOString(),
  // Status varies by test scenario
};
```

### Implementation Details

**Zombie Detection Criteria**:
- Trips created more than 35 minutes ago
- Trips with specific status that may have changed
- Trips without recent status updates

**API Integration Pattern**:
```javascript
const stubApiResponse = (code, data, requestId) => {
  nock(`${uberConfig.baseUrl}/trips/${requestId}`)
    .get(/.*/)
    .reply(code, data);
};
```

**Status Update Validation**:
```javascript
const checkTerminatedTripLogs = async (tripId) => {
  const trip = await Trips.query().where('id', tripId).first();
  const { ended_on: endedOn } = trip;
  expect(endedOn).not.to.be.null;
  
  const telework = await Teleworks.query().where('trip_id', tripId).first();
  const { ended_on: teleworkEndedOn } = telework;
  expect(teleworkEndedOn).not.to.be.null;
};
```

**Notification Validation**:
```javascript
const checkNotification = async (tripId, expectedMsg) => {
  const notification = await Notifications.query()
    .where('msg_data', 'like', `%"trip_id":${tripId}%`)
    .first();
  const msgData = JSON.parse(notification.msg_data);
  const { message } = msgData;
  expect(message).to.be.eq(expectedMsg);
  return notification.id;
};
```

**Incentive Testing Integration**:
- Tests incentive reward system for completed trips
- Validates user app version requirements (≥2.125.0)
- Ensures proper reward queue management

## Usage/Integration

### Test Execution

**Running Zombie Killer Tests**:
```bash
# Run complete zombie killer test suite
npm test test/testUberZombieKiller.js

# Run specific status transition scenarios
npm test test/testUberZombieKiller.js --grep "from processing"
npm test test/testUberZombieKiller.js --grep "incentive"
```

**Test Environment Requirements**:
- MySQL database with complete TSP schema
- Uber API configuration for trip status endpoints
- Mock HTTP server capabilities via Nock
- User management system for incentive testing

### Service Integration Flow

**Zombie Trip Processing Pipeline**:
1. **Stale Trip Detection**: Identify trips requiring status updates
2. **API Status Query**: Fetch current status from Uber API
3. **Status Comparison**: Compare API status with local database
4. **Database Updates**: Update trip status and related fields
5. **Business Logic**: Trigger notifications, incentives, termination logic
6. **Audit Logging**: Record all status changes and updates

**Key Service Method**:
```javascript
await uberServices.processZombieTrips();
```

### Integration Points

**Trip Lifecycle Management**:
- Trip status synchronization with Uber API
- Telework log updates and termination
- Notification delivery for status changes
- Incentive reward processing for completed trips

**External API Dependencies**:
- Uber trip details API endpoint
- Real-time status information retrieval
- Error handling for API failures

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with expect interface
- `mocha`: Test runner framework (implicit)

**HTTP Mocking**:
- `nock`: HTTP request interception for Uber API
- Mock response definitions for various trip statuses

**Utilities**:
- `uuid`: Unique request ID generation
- `moment-timezone`: Date/time manipulation for trip timing

### Database Dependencies

**Model Integration**:
- `Trips`: Core trip entity and lifecycle management
- `RidehailTrips`: Uber-specific trip data and status tracking
- `Teleworks`: Commute tracking and validation
- `TeleworkLogs`: Detailed trip activity logging
- `Notifications`: User communication system
- `AuthUsers`: User account management for incentives
- `IncentiveNotifyQueue`: Reward processing and tracking

### Business Logic Dependencies

**Service Integration**:
- `@app/src/services/uber/guest-ride`: Core Uber service
- Notification message templates
- Uber status definitions and state machine
- Incentive reward calculation logic

**Mock Data Sources**:
```javascript
const mockResource = require('@app/src/static/mock-data/ridehail');
const { notificationMessages } = require('../src/services/uber/guest-ride');
```

## Code Examples

### Basic Test Structure

```javascript
describe('Uber zombie-killer', () => {
  const checkTerminatedTripLogs = async (tripId) => {
    const trip = await Trips.query().where('id', tripId).first();
    const { ended_on: endedOn } = trip;
    expect(endedOn).not.to.be.null;
    
    const telework = await Teleworks.query().where('trip_id', tripId).first();
    const { ended_on: teleworkEndedOn } = telework;
    expect(teleworkEndedOn).not.to.be.null;
  };

  const checkNotification = async (tripId, expectedMsg) => {
    const notification = await Notifications.query()
      .where('msg_data', 'like', `%"trip_id":${tripId}%`)
      .first();
    const msgData = JSON.parse(notification.msg_data);
    const { message } = msgData;
    expect(message).to.be.eq(expectedMsg);
    return notification.id;
  };
});
```

### Status Transition Testing

```javascript
describe('from processing', () => {
  it('should update trip from processing to in_progress', async () => {
    // Setup mock data
    ids = await prepareMockData(requestId);
    const mockTripDetail = mockResource.getTripDetailsResponse;
    mockTripDetail.request_id = requestId;
    mockTripDetail.status = uberDefinitions.tripStatus.IN_PROGRESS;
    stubApiResponse(200, mockTripDetail, requestId);

    // Execute zombie killer
    await uberServices.processZombieTrips();

    // Validate status update
    const ridehailTrip = await RidehailTrips.query()
      .where('uber_request_id', requestId)
      .first();
      
    const {
      trip_status: tripStatus,
      pickup_eta: pEta,
      dropoff_eta: dEta,
      pickup_time: pTime,
    } = ridehailTrip;
    
    expect(tripStatus).to.be.eq(uberDefinitions.tripStatus.IN_PROGRESS);
    expect(pEta).to.be.eq(mockTripDetail.pickup.eta);
    expect(dEta).to.be.eq(mockTripDetail.destination.eta);
    expect(pTime).not.to.be.null;
  });

  it('should update trip from processing to completed', async () => {
    // Setup
    ids = await prepareMockData(requestId);
    const mockTripDetail = mockResource.completedTripDetailsResponse;
    mockTripDetail.request_id = requestId;
    mockTripDetail.status = uberDefinitions.tripStatus.COMPLETED;
    stubApiResponse(200, mockTripDetail, requestId);

    // Execute
    await uberServices.processZombieTrips();

    // Validate completion
    const ridehailTrip = await RidehailTrips.query()
      .where('uber_request_id', requestId)
      .first();
    const { trip_status: tripStatus } = ridehailTrip;
    expect(tripStatus).to.be.eq(uberDefinitions.tripStatus.COMPLETED);

    // Check trip termination
    await checkTerminatedTripLogs(ids[0]);

    // Verify notification
    const notificationId = await checkNotification(
      ids[0],
      notificationMessages.completed,
    );
    ids.push(notificationId);
  });
});
```

### Mock Data Preparation

```javascript
const prepareMockData = async (requestId, tripStatus = null) => {
  const now = moment().utc().toISOString();
  
  // Create trip with standard Houston locations
  const mockTrip = {
    user_id: userId,
    travel_mode: travelMode.RIDEHAIL,
    origin: '1015 S Shepherd Dr, Houston, TX 77019, US',
    destination: '6100 Main St, Houston, TX 77005, US',
    started_on: now,
  };
  const trip = await Trips.query().insert(mockTrip);

  // Create ridehail trip with zombie timing
  const mockRidehailTrip = {
    user_id: userId,
    trip_id: trip.id,
    uber_request_id: requestId,
    estimated_fare: 12.34,
    product_display_name: 'UberX',
    // Key: Created 35 minutes ago (zombie threshold)
    created_at: moment.utc().add(-35, 'minutes').toISOString(),
    updated_at: moment.utc().add(-35, 'minutes').toISOString(),
  };
  
  if (tripStatus) {
    mockRidehailTrip.trip_status = tripStatus;
  }

  // Create telework tracking with autolog flag
  const telework = await Teleworks.query().insert({
    user_id: userId,
    trip_date: moment(now).format('YYYY-MM-DD'),
    trip_id: trip.id,
    is_autolog: 1,  // Important for zombie detection
    created_on: now,
  });

  await RidehailTrips.query().insert(mockRidehailTrip);
  return [trip.id, requestId, telework.id, teleworkLog.id];
};
```

### Cancellation Scenario Testing

```javascript
it('should handle driver cancellation with refund setup', async () => {
  // Setup
  ids = await prepareMockData(requestId);
  const mockTripDetail = mockResource.driverCanceledTripDetailsResponse;
  mockTripDetail.request_id = requestId;
  mockTripDetail.status = uberDefinitions.tripStatus.DRIVER_CANCELED;
  stubApiResponse(200, mockTripDetail, requestId);

  // Execute
  await uberServices.processZombieTrips();

  // Validate cancellation processing
  const ridehailTrip = await RidehailTrips.query()
    .where('uber_request_id', requestId)
    .first();
    
  const { trip_status: tripStatus, payment_status: paymentStatus } = ridehailTrip;
  expect(tripStatus).to.be.eq(uberDefinitions.tripStatus.DRIVER_CANCELED);
  expect(paymentStatus).to.be.eq(
    uberDefinitions.paymentStatus.REFUND_IN_PROGRESS,
  );

  // Verify trip termination
  await checkTerminatedTripLogs(ids[0]);

  // Check notification
  const notificationId = await checkNotification(
    ids[0],
    notificationMessages.driver_canceled,
  );
  ids.push(notificationId);
});
```

### Incentive Reward Testing

```javascript
describe('incentive make-trip testing', () => {
  it('should receive reward after trip completed', async () => {
    // Setup user with qualifying app version
    await AuthUsers.query()
      .where('id', userId)
      .update({ app_version: '2.125.0' });
      
    ids = await prepareMockData(
      requestId,
      uberDefinitions.tripStatus.IN_PROGRESS,
    );

    // Mock completed trip with distance
    const mockTripDetail = mockResource.completedTripDetailsResponse;
    mockTripDetail.trip_distance_miles = 5.17;
    mockTripDetail.request_id = requestId;
    mockTripDetail.status = uberDefinitions.tripStatus.COMPLETED;
    stubApiResponse(200, mockTripDetail, requestId);

    // Execute zombie killer
    await uberServices.processZombieTrips();

    // Verify completion
    const ridehailTrip = await RidehailTrips.query()
      .where('uber_request_id', requestId)
      .first();
    expect(ridehailTrip.trip_status).to.be.eq(
      uberDefinitions.tripStatus.COMPLETED
    );

    // Check reward queue
    const reward = await IncentiveNotifyQueue.query()
      .select('points_transaction_id')
      .where('user_id', userId)
      .where('incentive_type', 'incentive make trip')
      .where('trip_ids', [ids[0]])
      .first();
    expect(reward).not.to.be.null;
  });
});
```

### No Records Validation

```javascript
describe('no records found', () => {
  it('should handle empty database gracefully', async () => {
    let failed;
    try {
      await uberServices.processZombieTrips();
    } catch (err) {
      failed = true;
    }
    expect(failed).not.to.be.true;
  });
});
```

This comprehensive test suite ensures the zombie killer service effectively maintains data synchronization between the local database and Uber's real-time API, preventing stale trip data while properly handling all status transitions, notifications, and business logic including incentive rewards for completed trips.