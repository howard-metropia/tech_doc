# test-reservations.js Technical Documentation

## Purpose

Comprehensive integration test suite for the reservation management system, covering trip planning, reservation creation, retrieval, and trip detail management.

## Core Functions

### Reservation Management

#### 1. Create Reservation
- **Route**: `createReservation`
- **Method**: POST
- **Payload**: Travel mode, origin/destination, timing details, trip UUID
- **Features**:
  - Creates reservations with trip details
  - Returns reservation ID and conflict offer IDs
  - Validates required fields and user authentication

#### 2. Get All Reservations  
- **Route**: `getReservations`
- **Method**: GET
- **Query Parameters**: `is_today`, `travel_mode`, pagination
- **Response Structure**:
  - `total_count`: Total reservation count
  - `next_offset`: Pagination offset
  - `reservations`: Array of reservation objects
  - `security_key`: Security validation key

#### 3. Get Trip Detail by ID
- **Route**: `getTripDetail/:id`
- **Method**: GET
- **Response**: Detailed trip information including sections and pricing

## Test Architecture

### Test Setup
```javascript
const userid = 1003;
const auth = { userid, 'Content-Type': 'application/json' };

// Test locations (Houston area)
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

### Test Data Dependencies
- **Intermodal Data**: Retrieves trip details from public transit API
- **Test Variables**: 
  - `tripDetailUuid`: From intermodal response
  - `travelMode`: Transit mode identifier
  - `reservationId`: Generated during creation tests

## Travel Mode Support

### DUO Mode Handling
- **Special Properties**: `riders`, `with_erh`, `premium`, `erh_available_time`
- **Role Validation**: Driver/rider role differences
- **Offer Management**: Shared offer IDs between participants

### Non-DUO Modes
- **Standard Properties**: Basic reservation fields
- **Travel Modes**: Walking, bicycling, driving, public transit, etc.

## Data Validation

### Reservation Object Structure
```javascript
const reservationKeys = [
  'id', 'travel_mode', 'role', 'origin', 'destination',
  'started_on', 'started_off', 'estimated_arrival_on',
  'estimated_arrival_off', 'overlap_on', 'overlap_off',
  'status', 'carpool_uuid', 'card_id', 'offer_id'
];
```

### Trip Detail Structure
```javascript
const tripDetailKeys = [
  'id', 'trip_detail_uuid', 'user_id', 'name',
  'reservation_id', 'trip_id', 'started_on', 'ended_on',
  'estimated_time', 'total_price', 'sections'
];
```

## Error Handling

### Authentication Errors
- **Code 10004**: Missing or invalid user ID in headers
- **Message**: "Request header has something wrong"

### Validation Errors  
- **Code 10002**: Missing required fields
- **Code 10001**: Invalid parameter format or values

### Data Errors
- **Code 20001**: Resource not found
- **Message**: "Data not found"

## Test Coverage

### Create Tests
1. **Successful Creation**: Valid reservation creation
2. **Authentication Failure**: Missing user ID
3. **Validation Failure**: Missing travel mode

### Retrieval Tests
1. **Successful Retrieval**: Get all reservations with filters
2. **Property Validation**: Verify response structure
3. **DUO Mode Handling**: Special case validation
4. **Authentication/Validation Errors**: Error scenarios

### Trip Detail Tests
1. **Successful Retrieval**: Get trip details by ID
2. **Not Found**: Invalid reservation ID
3. **Type Validation**: Non-numeric ID handling

## Integration Points

### External Dependencies
- **Intermodal Transit API**: Route planning and schedules
- **MongoDB**: Route history storage (`RoutesHistorys`)
- **MySQL**: Reservation and trip detail storage

### Model Interactions
- **Reservations**: Primary reservation model
- **TripDetails**: Associated trip information
- **RoutesHistorys**: MongoDB route storage

## Performance Considerations

### Test Timeouts
- **Standard Tests**: Default timeout
- **Intermodal Setup**: 20 second timeout for external API calls
- **Trip Detail Retrieval**: 10 second timeout for complex queries

### Cleanup Strategy
- **Route History**: MongoDB document deletion
- **Reservations**: MySQL record cleanup
- **Trip Details**: Associated record removal

## Security Features

### Authentication
- User ID validation in headers
- Request validation middleware

### Data Protection
- User-scoped data access
- Input sanitization and validation

## Usage Examples

### Creating a Reservation
```javascript
const input = {
  travel_mode: travelMode,
  name: 'unit test of reservation',
  origin: originObject,
  destination: destinationObject,
  started_on: startedOn,
  estimated_arrival_on: endedOn,
  trip_detail_uuid: tripDetailUuid,
};
```

### Querying Reservations
```javascript
// Get today's reservations
await request.set(auth).get(url).query({ is_today: true });

// Filter by travel mode
await request.set(auth).get(url).query({ travel_mode: [1, 2, 3] });
```

This test suite ensures robust reservation management functionality, covering creation, retrieval, validation, and error handling across multiple travel modes and user scenarios.