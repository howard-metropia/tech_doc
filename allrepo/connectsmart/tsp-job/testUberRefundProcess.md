# TSP Job Test: Uber Refund Process Integration Test Documentation

## Quick Summary

**Purpose**: Comprehensive integration test suite for Uber ride refund processing system, validating trip cancellation scenarios, receipt handling, and benefit credit calculations across the complete refund workflow.

**Key Features**:
- Tests `processRefundingTrips()` service for various cancellation scenarios
- Validates refund processing for rider and driver cancellations
- Handles receipt availability and absence scenarios
- Tests benefit credit integration (TIER1: $4, TIER2: $6, TIER3: $8)
- Comprehensive mock data management with realistic trip scenarios
- Integration with Uber API for receipt retrieval

**Technology Stack**: Mocha testing framework, Chai assertions, Nock for HTTP mocking, UUID generation, Moment.js for dates

## Technical Analysis

### Code Structure

The test file implements a comprehensive integration testing framework for Uber refund operations:

```javascript
// Core dependencies
const expect = require('chai').expect;
require('@maas/core/bootstrap');

// HTTP mocking and utilities
const nock = require('nock');
const moment = require('moment-timezone');
const { v4: uuidv4 } = require('uuid');

// Database models
const Trips = require('@app/src/models/Trips');
const Teleworks = require('@app/src/models/Teleworks');
const TeleworkLogs = require('@app/src/models/TeleworkLogs');
const RidehailTrips = require('@app/src/models/RidehailTrips');
const Notifications = require('@app/src/models/Notifications');

// Business services
const uberServices = require('@app/src/services/uber/guest-ride');
```

### Key Components

**Test Scenario Categories**:
1. **No Records**: Empty database scenarios
2. **Canceled with Receipts**: Uber provides receipt data
3. **Canceled without Receipts**: Uber returns 404 for receipt
4. **Canceled with Benefits**: Various benefit tier scenarios

**Mock Data Architecture**:
- Realistic trip data with Houston locations
- Complete telework log integration
- Uber-specific fields (request_id, product_id, guest_id)
- Benefit credit scenarios across three tiers

**HTTP Mock Integration**:
```javascript
const stubApiResponse = (code, data, requestId) => {
  nock(`${uberConfig.baseUrl}/trips/${requestId}/receipt`)
    .get(/.*/)
    .reply(code, data);
};
```

### Implementation Details

**Trip Data Structure**:
```javascript
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
```

**RidehailTrip Configuration**:
```javascript
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
  // Location details
  pickup: '1015 S Shepherd Dr, Houston, TX 77019, US',
  pickup_title: 'The Village of River Oaks',
  dropoff: '6100 Main St, Houston, TX 77005, US',
  dropoff_title: 'Rice University',
  // Status management
  trip_status: tripStatus,
  payment_status: uberDefinitions.paymentStatus.REFUND_IN_PROGRESS,
  benefit_credit: benefitCredit
};
```

**Benefit Credit Constants**:
```javascript
const BENEFIT_CREDITS = {
  TIER1: 4.0,  // $4 benefit
  TIER2: 6.0,  // $6 benefit
  TIER3: 8.0,  // $8 benefit
};
```

**Telework Integration**:
- Links trips to telework system for commute tracking
- Maintains distance and mile calculations
- Supports trip validation and audit trails

## Usage/Integration

### Test Execution

**Running Refund Process Tests**:
```bash
# Run complete refund process test suite
npm test test/testUberRefundProcess.js

# Run specific scenarios
npm test test/testUberRefundProcess.js --grep "canceled with receipts"
npm test test/testUberRefundProcess.js --grep "benefit credit"
```

**Test Environment Setup**:
- MySQL database with complete schema
- Uber API configuration for receipt endpoints
- Mock HTTP server for external API calls

### Service Integration Flow

**Refund Processing Pipeline**:
1. **Trip Identification**: Find trips requiring refund processing
2. **Receipt Retrieval**: Fetch receipt data from Uber API
3. **Fare Calculation**: Determine actual vs estimated fare differences
4. **Benefit Processing**: Apply benefit credits based on tier
5. **Database Updates**: Update trip status and payment information
6. **Notification Delivery**: Send refund confirmation to users
7. **Audit Logging**: Record all refund transactions

**Integration Points**:
```javascript
// Main refund processing
await uberServices.processRefundingTrips();

// Notification message validation
expect(msgData.message).to.be.eq(uberServices.notificationMessages.refunded);

// Payment status verification
expect(paymentStatus).to.be.eq(uberDefinitions.paymentStatus.REFUNDED);
```

### Mock Data Management

**Trip Creation Pattern**:
```javascript
const prepareMockData = async (
  requestId,
  tripStatus = null,
  benefitCredit = null,
) => {
  const now = moment().utc().toISOString();
  
  // Create trip record
  const trip = await Trips.query().insert(mockTrip);
  
  // Create ridehail trip with Uber specifics
  await RidehailTrips.query().insert(mockRidehailTrip);
  
  // Create telework tracking
  const telework = await Teleworks.query().insert({...});
  const teleworkLog = await TeleworkLogs.query().insert({...});
  
  return [trip.id, requestId, telework.id, teleworkLog.id];
};
```

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with expect interface
- `mocha`: Test runner framework (implicit)

**HTTP Mocking**:
- `nock`: HTTP request mocking for Uber API calls
- Mock resource definitions for various receipt scenarios

**Utilities**:
- `uuid`: Unique identifier generation for Uber request IDs
- `moment-timezone`: Date/time manipulation with timezone support

### Database Dependencies

**Model Requirements**:
- `Trips`: Core trip management and tracking
- `RidehailTrips`: Uber-specific trip data and status
- `Teleworks`: Commute tracking and validation
- `TeleworkLogs`: Detailed trip logging for audit
- `Notifications`: User communication and alerts

**Configuration Dependencies**:
- Uber API configuration (`config.vendor.uber`)
- Database connection settings
- Travel mode definitions and constants

### External Service Integration

**Uber API Integration**:
- Receipt endpoint for trip cost validation
- Authentication and request headers
- Error handling for API failures

**Business Logic Dependencies**:
- Currency conversion utilities
- Benefit credit calculation logic
- Notification message templates
- Trip status state machine

## Code Examples

### Basic Test Structure

```javascript
describe('uber refunding-trips process', () => {
  let requestId, ids, notificationId, mockTripDetails;
  
  const expectedToBe = async (totalFare) => {
    let failed;
    try {
      await uberServices.processRefundingTrips();
    } catch (err) {
      failed = true;
    }
    expect(failed).not.to.be.true;
    
    // Verify trip distance update
    const { distance: tripDistance } = await Trips.query()
      .where('id', ids[0])
      .first();
    expect(tripDistance).to.be.eq(0);
    
    // Verify ridehail trip updates
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

### Receipt Scenario Testing

```javascript
describe('canceled with receipts', () => {
  it('should handle rider canceled trips with receipt', async () => {
    // Setup mock data
    ids = await prepareMockData(
      requestId,
      uberDefinitions.tripStatus.RIDER_CANCELED,
    );
    
    // Mock Uber API response
    mockTripDetails = mockResource.canceledReceipt;
    mockTripDetails.request_id = requestId;
    stubApiResponse(200, mockTripDetails, requestId);
    
    // Execute and validate
    await expectedToBe(convertCurrencyToNumber(mockTripDetails.total_fare));
  });

  it('should handle driver canceled trips with receipt', async () => {
    ids = await prepareMockData(
      requestId,
      uberDefinitions.tripStatus.DRIVER_CANCELED,
    );
    
    mockTripDetails = mockResource.canceledReceipt;
    mockTripDetails.request_id = requestId;
    stubApiResponse(200, mockTripDetails, requestId);
    
    await expectedToBe(convertCurrencyToNumber(mockTripDetails.total_fare));
  });
});
```

### Benefit Credit Testing

```javascript
describe('canceled with benefit credit', () => {
  it('should handle TIER1 benefit when actual fare is less', async () => {
    // Setup with TIER1 benefit ($4)
    ids = await prepareMockData(
      requestId,
      uberDefinitions.tripStatus.RIDER_CANCELED,
      BENEFIT_CREDITS.TIER1,
    );

    // Mock receipt with fare less than benefit
    mockTripDetails = {
      ...mockResource.canceledReceipt,
      request_id: requestId,
      total_fare: '$3.00', // Actual fare < $4 benefit
    };

    stubApiResponse(200, mockTripDetails, requestId);

    let failed;
    try {
      await uberServices.processRefundingTrips();
    } catch (err) {
      failed = true;
    }
    expect(failed).not.to.be.true;

    // Verify benefit processing
    const rideHailTrips = await RidehailTrips.query()
      .where('uber_request_id', requestId)
      .first();

    expect(rideHailTrips.payment_status).to.be.eq(
      uberDefinitions.paymentStatus.REFUNDED,
    );
    expect(Number(rideHailTrips.actual_fare)).to.be.eq(3.0);
    expect(Number(rideHailTrips.benefit_credit)).to.be.eq(
      BENEFIT_CREDITS.TIER1,
    );
  });
});
```

### No Receipt Scenario Testing

```javascript
describe('canceled without receipt', () => {
  it('should handle cancellation when Uber has no receipt', async () => {
    ids = await prepareMockData(
      requestId,
      uberDefinitions.tripStatus.RIDER_CANCELED,
    );
    
    // Mock 404 response from Uber
    mockTripDetails = mockResource.receiptNotFoundResponse;
    stubApiResponse(404, mockTripDetails, requestId);
    
    // Should still process with zero fare
    await expectedToBe(0);
  });
});
```

### Notification Validation

```javascript
// Validate refund notification
const notification = await Notifications.query()
  .where('msg_data', 'like', `%"trip_id":${ids[0]}%`)
  .first();

notificationId = notification.id;
ids.push(notificationId);

const msgData = JSON.parse(notification.msg_data);
expect(msgData.message).to.be.eq(
  uberServices.notificationMessages.refunded,
);
```

### Data Cleanup Pattern

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

This comprehensive test suite ensures the Uber refund processing system correctly handles all cancellation scenarios, from simple refunds without receipts to complex benefit credit calculations, while maintaining data integrity across multiple related database tables and external API integrations.