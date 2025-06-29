# test-instant-carpoolings.js Technical Documentation

## Purpose

Comprehensive integration test suite for the instant carpooling system, covering the complete carpooling lifecycle from creation to completion, including driver-rider interactions and trip management.

## Core Functionality

### Instant Carpooling Lifecycle

#### 1. Create Carpool Offer
- **Route**: `createInstantCarpooling`
- **Method**: POST
- **Actor**: Driver
- **Payload**: Origin, destination, travel time
- **Returns**: Carpool ID for subsequent operations

#### 2. Join Carpool
- **Route**: `joinInstantCarpooling/:id`
- **Method**: PATCH
- **Actor**: Rider
- **Result**: Matches rider with driver

#### 3. Leave Carpool
- **Route**: `leaveInstantCarpooling/:id`
- **Method**: PATCH
- **Actor**: Driver (can remove riders)
- **Payload**: `rider_id` to remove

#### 4. Start Trip
- **Route**: `startInstantCarpooling/:id`
- **Method**: PATCH
- **Actor**: Driver
- **Payload**: `estimated_arrival_on`

#### 5. Finish Trip
- **Route**: `finishInstantCarpooling/:id`
- **Method**: PATCH
- **Actor**: Driver
- **Payload**: Distance, final arrival time

#### 6. Rate Experience
- **Route**: `commentInstantCarpooling/:id`
- **Method**: PATCH
- **Actor**: Both parties
- **Payload**: Rating (1-5), feedback text

## Test Architecture

### User Setup
```javascript
const driverId = 1005;
const riderId = 1003;
let driverAuth = { userid: driverId, 'Content-Type': 'application/json' };
let riderAuth = { userid: riderId, 'Content-Type': 'application/json' };
```

### JWT Token Management
- **Token Generation**: Creates valid JWT tokens for test users
- **Token Storage**: Updates `auth_user_tokens` table
- **Authorization Headers**: Bearer token authentication

### Market Validation
- **Market Assignment**: Both users assigned to 'HCS' market
- **Market Cleanup**: Restored to 'general' market after tests

## Trip Data Structure

### Location Objects
```javascript
const origin = {
  name: 'Houston',
  address: 'Houston, TX, USA',
  access_latitude: 29.7604267,
  access_longitude: -95.3698028,
  latitude: 29.7604267,
  longitude: -95.3698028,
};

const destination = {
  name: 'Houston Zoo',
  address: '6200 Hermann Park Dr, Houston, TX 77030, United States',
  access_latitude: 29.7345739,
  access_longitude: -95.4392542,
  latitude: 29.7345739,
  longitude: -95.4392542,
};
```

### Trip Parameters
- **Travel Time**: 1200 seconds (20 minutes)
- **Distance**: 3220 meters
- **Estimated Arrival**: 30 minutes from creation

## Carpool States and Transitions

### State Flow
1. **Created**: Driver creates offer
2. **Waiting**: Available for riders to join
3. **Matched**: Rider has joined
4. **Active**: Trip started by driver
5. **Finished**: Trip completed
6. **Rated**: Feedback provided

### Status Tracking
- **Driver History**: Shows completion status
- **Rider History**: Shows participation status
- **Completion Types**: COMPLETED, INCOMPLETE, CANCELED

## API Response Structures

### Get Carpool Details
```javascript
const carpoolDetails = {
  status: 'waiting',
  riders: [{
    user_id: 1003,
    first_name: 'passenger',
    last_name: 'duo',
    avatar: 'avatar_url'
  }],
  security_key: 'validation_key'
};
```

### History Response
```javascript
const historyItem = {
  trip_id: 'trip_identifier',
  role: 'driver' | 'rider',
  completion: 'COMPLETED' | 'INCOMPLETE' | 'CANCELED',
  started_on: 'timestamp',
  ended_on: 'timestamp',
  destination: destinationObject,
  match_type: 'instant',
  status: 'trip_status',
  riders: [riderObjects]
};
```

## MongoDB Integration

### Document Storage
- **Model**: `InstantCarpoolings`
- **Structure**: Driver and rider information
- **Trip IDs**: Generated for incentive tracking

### Data Management
```javascript
// Cleanup example
await InstantCarpoolings.deleteOne({
  'driver.userId': driverId,
});
```

## Error Handling

### Authentication Errors
- **Code 10003**: Missing or invalid Bearer token
- **Message**: "Token required"

### Validation Errors
- **Code 10002**: Missing required fields or invalid format
- **Code 10001**: Invalid parameter values

### Business Logic Errors
- **Code 25002**: Carpool not found
- **Code 20022**: Data not found (generic)

### MongoDB Pattern Validation
- **Pattern**: `/^[0-9a-fA-F]{24}$/`
- **Purpose**: Validates MongoDB ObjectId format

## Incentive Integration

### Trip ID Generation
- Driver and rider receive separate trip IDs
- Trip IDs used for incentive notifications
- Stored in `incentive_notify_queue`

### Cleanup Requirements
```javascript
// Remove incentive records
await knex('incentive_notify_queue')
  .where({ user_id: driverId, trip_ids: result.driver.tripId })
  .delete();
```

## Test Coverage Scenarios

### Creation Tests
1. **Successful Creation**: Valid carpool creation
2. **Authentication Failure**: Missing token
3. **Validation Failure**: Missing origin/destination

### Join/Leave Tests
1. **Successful Join**: Rider joins carpool
2. **Successful Leave**: Driver removes rider
3. **Error Cases**: Invalid IDs, missing participants

### Trip Management Tests
1. **Start Trip**: Driver initiates journey
2. **Finish Trip**: Complete with distance/time
3. **Rating System**: Post-trip feedback

### History Tests
1. **Driver History**: Shows created carpools
2. **Rider History**: Shows joined carpools
3. **Status Progression**: Tracks completion states

## Performance Considerations

### Test Timeouts
- **Standard Operations**: 5 second timeout
- **Trip Comments**: Default timeout for rating operations

### Data Volume
- **Concurrent Carpools**: Multiple active carpools per user
- **History Management**: Efficient pagination of trip history

## Trajectory Tracking (Commented)

### GPS Upload System
```javascript
// Trajectory upload capability (disabled in tests)
const trajectory = {
  mode: "instant_carpool",
  trip_id: tripId,
  trajectory: [{
    latitude: 25.049880981445312,
    longitude: 121.52930630401991,
    altitude: 10,
    course: 178,
    speed: 30,
    accuracy: 54,
    timestamp: timestamp
  }]
};
```

### Validation Requirements
- **Minimum Points**: 40 trajectory uploads required
- **Time Intervals**: 4-5 second intervals between uploads
- **Data Format**: Gzipped JSON payload

## Security Features

### Token Validation
- JWT token verification
- User-specific data access
- Market-based restrictions

### Data Protection
- User ID validation in all operations
- Carpool owner permissions
- Secure trip data handling

## Integration Points

### External Dependencies
- **Authentication Service**: JWT token validation
- **Incentive System**: Trip reward processing
- **Market System**: User market assignment

### Database Systems
- **MongoDB**: Carpool document storage
- **MySQL**: User management and incentives

## Usage Examples

### Creating a Carpool
```javascript
const carpoolData = {
  origin: originObject,
  destination: destinationObject,
  travel_time: 1200
};

const response = await request
  .set(driverAuth)
  .post('/api/v2/instant-carpoolings')
  .send(carpoolData);
```

### Joining a Carpool
```javascript
const response = await request
  .set(riderAuth)
  .patch(`/api/v2/instant-carpoolings/${carpoolId}`)
  .send();
```

This test suite ensures robust instant carpooling functionality, covering the complete user journey from carpool creation through trip completion and rating, with comprehensive error handling and data validation.