# TSP Job Test: Uber Rider Canceled Process Integration Test Documentation

## Quick Summary

**Purpose**: Focused integration test suite for Uber rider-canceled trip processing, specifically testing the `processRiderCanceledTrips()` service workflow for handling trips canceled by passengers.

**Key Features**:
- Tests rider-specific cancellation processing logic
- Validates receipt retrieval and processing for canceled trips  
- Handles both receipt-available and receipt-not-found scenarios
- Comprehensive database state validation across multiple tables
- Integration with Uber API for receipt data retrieval
- Notification system validation for user communication

**Technology Stack**: Mocha testing framework, Chai assertions, Nock for HTTP mocking, UUID generation, Moment.js for dates

## Technical Analysis

### Code Structure

The test file implements a streamlined testing framework focused on rider cancellation scenarios:

```javascript
// Core testing dependencies
const expect = require('chai').expect;
require('@maas/core/bootstrap');

// HTTP mocking and utilities  
const nock = require('nock');
const moment = require('moment-timezone');
const { v4: uuidv4 } = require('uuid');

// Database models for trip lifecycle
const Trips = require('@app/src/models/Trips');
const Teleworks = require('@app/src/models/Teleworks');
const TeleworkLogs = require('@app/src/models/TeleworkLogs');
const RidehailTrips = require('@app/src/models/RidehailTrips');
const Notifications = require('@app/src/models/Notifications');

// Uber service integration
const uberServices = require('@app/src/services/uber/guest-ride');
```

### Key Components

**Test Scope Focus**:
- Exclusively tests rider-canceled trip scenarios
- Validates `processRiderCanceledTrips()` service method
- Covers receipt availability and absence handling
- Ensures proper database state transitions

**Mock Data Architecture**:
```javascript
const mockRidehailTrip = {
  // ... trip details
  trip_status: uberDefinitions.tripStatus.RIDER_CANCELED,
  payment_status: uberDefinitions.paymentStatus.REFUND_IN_PROGRESS,
  created_at: moment.utc().add(-6, 'hours').toISOString(),
  updated_at: moment.utc().add(-5, 'hours').toISOString(),
};
```

**API Mock Integration**:
- Uses Nock to mock Uber receipt endpoint
- Supports both successful (200) and not-found (404) responses
- Validates request/response cycle for receipt retrieval

### Implementation Details

**Test Scenario Categories**:
1. **No Records**: Empty database validation
2. **Canceled with Receipts**: Successful receipt retrieval
3. **Canceled without Receipts**: 404 receipt scenarios

**Trip Status Management**:
- Fixed to `RIDER_CANCELED` status for all test scenarios
- Payment status set to `REFUND_IN_PROGRESS` initially
- Validates transition to `REFUNDED` status after processing

**Database Validation Pattern**:
```javascript
const expectedToBe = async (totalFare) => {
  await uberServices.processRiderCanceledTrips();
  
  // Trip distance validation
  const { distance: tripDistance } = await Trips.query()
    .where('id', ids[0])
    .first();
  expect(tripDistance).to.be.eq(0);
  
  // Ridehail trip status validation
  const rideHailTrips = await RidehailTrips.query()
    .where('uber_request_id', requestId)
    .first();
    
  expect(rideHailTrips.payment_status).to.be.eq(
    uberDefinitions.paymentStatus.REFUNDED
  );
  expect(Number(rideHailTrips.actual_fare)).to.be.eq(totalFare);
};
```

**Notification Validation**:
- Verifies notification creation for refunded trips
- Validates message content matches expected refund message
- Ensures proper user targeting for notifications

## Usage/Integration

### Test Execution

**Running Rider Canceled Tests**:
```bash
# Run rider cancellation test suite
npm test test/testUberRiderCanceledProcess.js

# Run with verbose output
npm test test/testUberRiderCanceledProcess.js --reporter spec
```

**Test Environment Requirements**:
- MySQL database with complete TSP schema
- Uber API configuration for receipt endpoints
- Mock HTTP server capabilities via Nock

### Service Integration

**Core Service Method**:
```javascript
// Main service method being tested
await uberServices.processRiderCanceledTrips();
```

**Integration Points**:
- Uber receipt API endpoint integration
- Database transaction management
- Notification system integration
- Telework logging system

**Expected Database Changes**:
- Trip distance reset to 0
- Receipt distance and duration set to 0
- Payment status updated to REFUNDED
- Actual fare recorded from receipt or set to 0
- Telework log mileage updated accordingly

### API Mock Configuration

**Receipt Endpoint Mocking**:
```javascript
const stubApiResponse = (code, data, requestId) => {
  nock(`${uberConfig.baseUrl}/trips/${requestId}/receipt`)
    .get(/.*/)
    .reply(code, data);
};
```

**Mock Response Scenarios**:
- **200 Success**: Returns complete receipt with fare details
- **404 Not Found**: Receipt not available (common for quick cancellations)

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with expect interface
- `mocha`: Test runner framework (implicit)

**HTTP Mocking**:
- `nock`: HTTP request interception and mocking
- Mock response data from predefined resources

**Utilities**:
- `uuid`: Unique request ID generation for test isolation
- `moment-timezone`: Date/time manipulation for trip timestamps

### Database Dependencies

**Model Integration**:
- `Trips`: Core trip entity management
- `RidehailTrips`: Uber-specific trip data and status tracking
- `Teleworks`: Commute tracking integration
- `TeleworkLogs`: Detailed audit trail for trip activities
- `Notifications`: User communication system

**Business Logic Dependencies**:
- `@app/src/services/uber/guest-ride`: Core Uber service integration
- Currency conversion utilities (`convertCurrencyToNumber`)
- Uber status definitions and constants
- Travel mode enumeration

### Configuration Dependencies

**Uber API Configuration**:
```javascript
const config = require('config');
const uberConfig = config.vendor.uber;
```

**Mock Resource Integration**:
```javascript
const mockResource = require('@app/src/static/mock-data/ridehail');
```

## Code Examples

### Basic Test Structure

```javascript
describe('uber rider-canceled trips refunding process', () => {
  let requestId, ids, notificationId, mockTripDetails;
  
  const stubApiResponse = (code, data, requestId) => {
    nock(`${uberConfig.baseUrl}/trips/${requestId}/receipt`)
      .get(/.*/)
      .reply(code, data);
  };
  
  const expectedToBe = async (totalFare) => {
    await uberServices.processRiderCanceledTrips();
    
    // Validate trip updates
    const { distance: tripDistance } = await Trips.query()
      .where('id', ids[0])
      .first();
    expect(tripDistance).to.be.eq(0);
    
    // Validate ridehail trip status
    const rideHailTrips = await RidehailTrips.query()
      .where('uber_request_id', requestId)
      .first();
      
    const {
      receipt_distance: distance,
      receipt_duration: duration,
      actual_fare: aFare,
      payment_status: paymentStatus,
    } = rideHailTrips;
    
    expect(distance).to.be.eq(0);
    expect(duration).to.be.eq(0);
    expect(paymentStatus).to.be.eq(uberDefinitions.paymentStatus.REFUNDED);
    expect(Number(aFare)).to.be.eq(totalFare);
  };
});
```

### Mock Data Preparation

```javascript
const prepareMockData = async (requestId) => {
  const now = moment().utc().toISOString();
  
  // Create base trip record
  const mockTrip = {
    user_id: userId,
    travel_mode: travelMode.RIDEHAIL,
    origin: '1015 S Shepherd Dr, Houston, TX 77019, US',
    origin_latitude: startLocation[0],
    origin_longitude: startLocation[1],
    started_on: now,
    destination: '6100 Main St, Houston, TX 77005, US',
    destination_latitude: endLocation[0],
    destination_longitude: endLocation[1],
  };
  const trip = await Trips.query().insert(mockTrip);

  // Create ridehail trip with RIDER_CANCELED status
  const mockRidehailTrip = {
    user_id: userId,
    trip_id: trip.id,
    uber_fare_id: uuidv4(),
    uber_request_id: requestId,
    uber_product_id: uuidv4(),
    estimated_fare: 12.34,
    product_display_name: 'UberX',
    uber_guest_id: uuidv4(),
    guest_phone_number: '+1234567890',
    // Pre-set to rider canceled status
    trip_status: uberDefinitions.tripStatus.RIDER_CANCELED,
    payment_status: uberDefinitions.paymentStatus.REFUND_IN_PROGRESS,
    created_at: moment.utc().add(-6, 'hours').toISOString(),
    updated_at: moment.utc().add(-5, 'hours').toISOString(),
  };
  
  // Create telework tracking
  const telework = await Teleworks.query().insert({
    user_id: userId,
    trip_date: moment(now).format('YYYY-MM-DD'),
    trip_id: trip.id,
    created_on: now,
    modified_on: now,
    started_on: now,
  });
  
  const teleworkLog = await TeleworkLogs.query().insert({
    telework_id: telework.id,
    travel_mode: 'ridehail',
    origin_name: mockTrip.origin,
    destination_name: mockTrip.destination,
    created_on: now,
  });
  
  await RidehailTrips.query().insert(mockRidehailTrip);
  return [trip.id, requestId, telework.id, teleworkLog.id];
};
```

### Receipt Available Scenario

```javascript
describe('canceled with receipts', () => {
  it('should process rider canceled trip with receipt', async () => {
    // Setup mock data
    ids = await prepareMockData(requestId);
    
    // Mock successful receipt response
    mockTripDetails = mockResource.canceledReceipt;
    mockTripDetails.request_id = requestId;
    stubApiResponse(200, mockTripDetails, requestId);
    
    // Execute and validate
    await expectedToBe(convertCurrencyToNumber(mockTripDetails.total_fare));
  });
});
```

### Receipt Not Found Scenario

```javascript
describe('canceled without receipt', () => {
  it('should handle rider cancellation without receipt', async () => {
    // Setup mock data
    ids = await prepareMockData(requestId);
    
    // Mock 404 response (no receipt available)
    mockTripDetails = mockResource.receiptNotFoundResponse;
    stubApiResponse(404, mockTripDetails, requestId);
    
    // Should process with zero fare
    await expectedToBe(0);
  });
});
```

### Notification Validation

```javascript
// Validate notification creation and content
const teleworkLog = await TeleworkLogs.query().where('id', ids[3]).first();
const { distance: logDistance, mile } = teleworkLog;
expect(logDistance).to.be.eq(0);
expect(mile).to.be.eq(0);

const notification = await Notifications.query()
  .where('msg_data', 'like', `%"trip_id":${ids[0]}%`)
  .first();
  
notificationId = notification.id;
ids.push(notificationId);

const msgData = JSON.parse(notification.msg_data);
const { message } = msgData;
expect(message).to.be.eq(uberServices.notificationMessages.refunded);
```

### No Records Validation

```javascript
describe('no records', () => {
  it('should pass when no rider canceled records found', async () => {
    let failed;
    try {
      await uberServices.processRiderCanceledTrips();
    } catch (err) {
      failed = true;
    }
    expect(failed).not.to.be.true;
  });
});
```

### Cleanup Pattern

```javascript
const cleanUpMockData = async (ids) => {
  if (ids.length > 0) {
    await Trips.query().where('id', ids[0]).delete();
    await Teleworks.query().where('id', ids[2]).delete();
    await TeleworkLogs.query().where('id', ids[3]).delete();
    await Notifications.query().where('id', ids[4]).delete();
  }
};

afterEach(async () => {
  await cleanUpMockData(ids);
});
```

This focused test suite ensures the rider cancellation processing system correctly handles all scenarios specific to passenger-initiated trip cancellations, from receipt processing to database updates and user notifications, while maintaining data integrity across the complete trip lifecycle.