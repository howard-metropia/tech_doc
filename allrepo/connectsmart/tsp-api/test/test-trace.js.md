# test-trace.js

## Overview
Comprehensive test suite for user activity tracing and analytics in the TSP API. Tests user visit tracking, ETA change notifications, and carpool-specific trip management with role-based permissions.

## File Location
`/test/test-trace.js`

## Dependencies
- **@maas/core**: Core MaaS framework components
- **supertest**: HTTP assertions for API testing
- **uuid**: UUID generation and validation
- **chai**: BDD/TDD assertion library
- **sinon**: Test spies, stubs, and mocks
- **Models**: Trips, DuoReservations, TripRoutes, TripValidationQueue
- **Database**: MongoDB integration

## Test Structure

### Setup and Cleanup
```javascript
let sandbox;

beforeEach(() => {
  sandbox = sinon.createSandbox();
});

afterEach(() => {
  sandbox.restore();
});
```

## Test Suites

### 1. User Visit Tracking

#### POST user_visit
**Endpoint**: `POST /user-visit`

**Request Data**:
```javascript
{
  latitude: 22.34567799,
  longitude: 100.23112299,
  arrival_date: 1539769544,      // Unix timestamp
  departure_date: 1539773143,    // Unix timestamp
  os_type: 'integration test'
}
```

**Test Configuration**:
- **User ID**: 9999
- **Expected Status**: 200
- **Purpose**: Track user location visits for analytics

### 2. ETA Change Management

#### Test Data Setup
```javascript
const tripId = 12345;
const userId = 9999;
const newETA = '2025-06-16T15:30:00Z';
```

#### Database Mocking Strategy
```javascript
// Trip lookup mock
sandbox.stub(Trips, 'query').returns({
  findById: sandbox.stub().resolves({
    id: tripId,
    user_id: userId,
    travel_mode: 1,
    reservation_id: null
  })
});

// Route insertion mock
sandbox.stub(TripRoutes, 'query').returns({
  insert: sandbox.stub().resolves({})
});

// Validation queue mock
sandbox.stub(TripValidationQueue, 'query').returns({
  where: sandbox.stub().returns({
    andWhere: sandbox.stub().returns({
      first: sandbox.stub().resolves(null)
    })
  }),
  insert: sandbox.stub().resolves({})
});
```

## ETA Change Test Cases

### 1. Regular Trip ETA Update
**Travel Mode**: 1 (regular driving)

**Test Flow**:
1. Send ETA update request
2. Verify TripRoutes.insert called
3. Confirm 200 response

**Expected Behavior**:
- ETA update processed normally
- Route data inserted into TripRoutes
- No special role checking required

### 2. Scheduled Carpool (DUO) - Driver
**Travel Mode**: 100 (DUO scheduled carpool)
**User Role**: 1 (driver)

**Mock Setup**:
```javascript
// Trip with reservation
Trips.query().findById.resolves({
  id: tripId,
  user_id: userId,
  travel_mode: 100,
  reservation_id: 'res-123'
});

// Driver role in reservation
sandbox.stub(DuoReservations, 'query').returns({
  where: sandbox.stub().returns({
    first: sandbox.stub().resolves({
      reservation_id: 'res-123',
      role: 1  // Driver
    })
  })
});
```

**Expected Behavior**:
- ETA update processed (drivers can update ETA)
- Route data inserted
- 200 response with successful processing

### 3. Scheduled Carpool (DUO) - Passenger
**Travel Mode**: 100 (DUO scheduled carpool)
**User Role**: 2 (passenger)

**Mock Setup**:
```javascript
// Passenger role in reservation
sandbox.stub(DuoReservations, 'query').returns({
  where: sandbox.stub().returns({
    first: sandbox.stub().resolves({
      reservation_id: 'res-123',
      role: 2  // Passenger
    })
  })
});
```

**Expected Behavior**:
- ETA update received but not processed
- No route data insertion
- 200 response with message: "Only driver's ETA updates"

### 4. Instant Carpool - Driver
**Travel Mode**: 101 (INSTANT_CARPOOL)
**User Role**: Driver

**MongoDB Mock Setup**:
```javascript
sandbox.stub(mongodb, 'db').value({
  collection: sandbox.stub().returns({
    findOne: sandbox.stub().resolves({
      driver: { tripId: tripId }  // User is the driver
    })
  })
});
```

**Expected Behavior**:
- ETA update processed (driver permission)
- Route data inserted
- 200 response

### 5. Instant Carpool - Passenger
**Travel Mode**: 101 (INSTANT_CARPOOL)
**User Role**: Passenger

**MongoDB Mock Setup**:
```javascript
sandbox.stub(mongodb, 'db').value({
  collection: sandbox.stub().returns({
    findOne: sandbox.stub()
      .onCall(0).resolves(null)  // Not in driver collection
      .onCall(1).resolves({      // Found in riders collection
        riders: [{ tripId: tripId }]
      })
  })
});
```

**Expected Behavior**:
- ETA update received but not processed
- No route data insertion
- 200 response with message: "Only driver's ETA updates"

## Error Handling Test Cases

### 1. Missing Required Parameters
**Test**: Send request without ETA or route data

**Expected Response**:
- Status: 400 (Bad Request)
- Validates required parameters

### 2. Trip Not Found
**Test**: Request ETA update for non-existent trip

**Mock Setup**:
```javascript
Trips.query().findById.resolves(null);
```

**Expected Response**:
- Status: 404 (Not Found)
- Trip doesn't exist in database

## Travel Mode Classification

### Travel Mode Values
- **1**: Regular driving
- **100**: DUO (scheduled carpool)
- **101**: INSTANT_CARPOOL (real-time carpool)

### Role Classification
- **DUO Carpool Roles**:
  - Role 1: Driver (can update ETA)
  - Role 2: Passenger (cannot update ETA)

- **Instant Carpool Roles**:
  - Driver: Found in driver collection
  - Passenger: Found in riders collection

## Database Integration

### MySQL Models
- **Trips**: Trip information and metadata
- **DuoReservations**: Scheduled carpool reservations
- **TripRoutes**: Route and ETA update history
- **TripValidationQueue**: Trip validation processing

### MongoDB Collections
- **Instant Carpool**: Real-time carpool matching data
- **Driver/Rider Collections**: Role assignment for instant carpools

## Business Logic

### ETA Update Rules
1. **Regular Trips**: All users can update ETA
2. **Scheduled Carpool**: Only drivers can update ETA
3. **Instant Carpool**: Only drivers can update ETA
4. **Passengers**: Receive acknowledgment but no processing

### Permission System
- **Role-based Access**: Driver vs. passenger permissions
- **Trip Type Awareness**: Different rules for different carpool types
- **Database Lookups**: Role verification through multiple data sources

## Analytics and Tracking

### User Visit Data
- **Location Tracking**: Latitude/longitude coordinates
- **Time Tracking**: Arrival and departure timestamps
- **Device Information**: OS type for analytics
- **User Association**: Linked to authenticated user

### ETA Change Analytics
- **Trip Correlation**: Links ETA changes to specific trips
- **Role Tracking**: Records whether driver or passenger initiated change
- **Validation Queue**: Processes ETA changes for validation

## API Response Patterns

### Success Response
```javascript
{
  result: "success",
  data: {
    message: "ETA updated successfully"
  }
}
```

### Permission Denied Response
```javascript
{
  result: "success",
  data: {
    message: "Only driver's ETA updates are processed"
  }
}
```

### Error Response
```javascript
{
  result: "fail",
  error: {
    code: 400,
    message: "Missing required parameters"
  }
}
```

## Testing Strategy

### Comprehensive Mocking
- **Database Operations**: Complete mock coverage
- **External Services**: MongoDB and MySQL mocking
- **Role Verification**: Multi-source role checking

### Edge Case Coverage
- **Permission Scenarios**: Driver vs. passenger access
- **Error Conditions**: Missing data, invalid trips
- **Carpool Types**: Both scheduled and instant carpool testing

### Integration Testing
- **Full Request Cycle**: End-to-end API testing
- **Real Data Structures**: Authentic request/response formats
- **Authentication**: User ID-based request authentication

This test suite ensures the trace system accurately tracks user activities, properly manages ETA updates with role-based permissions, and maintains data integrity across different carpool scenarios in the TSP API's analytics and tracking features.