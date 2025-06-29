# TSP API Test Suite - Trip Management Core Tests

## Overview
The `test-trip.js` file contains comprehensive unit and integration tests for the core trip lifecycle management functionality in the TSP API. This test suite validates the complete journey from trip initiation to completion, ensuring reliable transportation service operations.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-trip.js`

## Dependencies
- **@maas/core**: Core MaaS framework components
- **chai/mocha**: Testing framework and assertions
- **supertest**: HTTP assertion library
- **uuid**: Unique identifier generation
- **moment-timezone**: Date/time manipulation

## Test Architecture

### Core Models
- `Trip`: Primary trip management model
- `Reservations`: Trip reservation system
- `TeleworkLogTmps`: Temporary telework logging
- `Teleworks`: Telework management
- `TeleworkLogs`: Telework activity logging
- `TripWaypoints`: Trip route waypoint management

### Service Layer
- `startTrip`: Trip initiation service
- `endTrip`: Trip completion service
- `getTrips`: Trip retrieval service
- `getTripCount`: Trip statistics service
- `getTripDetails`: Detailed trip information service

## Test Categories

### 1. Unit Tests for Start Trip

**Test Subject**: `startTrip` service function

**Test Scenarios**:
- **Normal Driving Trip (No Reservation)**
  - Creates trip with origin/destination coordinates
  - Validates travel mode, timing, and navigation app
  - Verifies database persistence and field mapping
  
- **Normal Driving Trip (With Reservation)**
  - Links trip to existing reservation
  - Validates reservation integration
  - Tests role-based trip creation

**Key Validations**:
```javascript
// Trip field validation
expect(trip).has.property('user_id', userId);
expect(trip).has.property('travel_mode', travel_mode);
expect(trip).has.property('origin_latitude', input.origin.latitude);
expect(trip).has.property('destination_longitude', input.destination.longitude);
expect(trip).has.property('trip_detail_uuid', trip_detail_uuid);
expect(trip).has.property('navigation_app', navAppMap[input.navigation_app]);
```

### 2. Unit Tests for End Trip

**Test Subject**: `endTrip` service function

**Test Scenarios**:
- **Successful Trip Completion**
  - Updates trip end time and distance
  - Calculates trip metrics
  - Validates final trip state

**Response Structure**:
```javascript
{
  user_id: number,
  trip_id: number,
  mode: string,
  origin: { latitude, longitude },
  destination: { latitude, longitude }
}
```

### 3. Integration Tests for End Trip

**Test Subject**: Full HTTP endpoint testing

**API Endpoints Tested**:
- Trip creation via REST API
- Trip completion via REST API
- Authentication and authorization

**Integration Flow**:
1. Create trip via API endpoint
2. Validate trip creation response
3. End trip via API endpoint
4. Verify complete trip lifecycle

## Trip Data Structure

### Input Parameters (Start Trip)
```javascript
{
  userId: number,
  travel_mode: number,
  is_calendar_event: boolean,
  origin: {
    name: string,
    address: string,
    latitude: number,
    longitude: number
  },
  destination: {
    name: string,
    address: string,  
    latitude: number,
    longitude: number
  },
  started_on: datetime,
  estimated_arrival_on: datetime,
  trip_detail_uuid: string,
  navigation_app: string,
  reservation_id?: number
}
```

### Trip Database Schema Validation
- **Required Fields**: user_id, travel_mode, origin coordinates, destination coordinates
- **Optional Fields**: reservation_id, role, card_id
- **Calculated Fields**: distance, trajectory_distance, end_status
- **Metadata**: trip_detail_uuid, navigation_app, local_time

## Navigation App Mapping
```javascript
const navAppMap = {
  here: 1,
  google: 2,
  apple: 3,
  waze: 4
}
```

## Travel Modes
- **1**: Driving
- **2**: Public Transit
- **3**: Walking
- **4**: Biking
- **5**: Intermodal
- **100**: Duo (Carpool)

## Key Features Tested

### 1. Trip Lifecycle Management
- Trip creation with comprehensive field validation
- Trip state management throughout journey
- Trip completion with metric calculation

### 2. Reservation Integration
- Optional reservation linking
- Reservation status validation
- Role-based trip assignment

### 3. Location Services
- Origin/destination coordinate handling
- Navigation app integration
- Real-time location tracking setup

### 4. Temporal Management
- Start time recording
- Estimated arrival time tracking
- Trip duration calculation
- Timezone handling

### 5. Telework Integration
- Temporary telework log creation
- Work-related trip classification
- Calendar event integration

## Test Data Management

**Setup Process**:
- Generate unique trip_detail_uuid for each test
- Create test reservation if needed
- Prepare mock location data

**Cleanup Process**:
- Remove created trips from database
- Clean up telework temporary logs
- Delete test reservations

## Error Handling

**Validation Coverage**:
- Missing required parameters
- Invalid coordinate ranges
- Unsupported travel modes
- Authentication failures
- Database constraint violations

## Performance Considerations

**Test Optimization**:
- Efficient test data setup/teardown
- Minimal database operations
- Isolated test scenarios
- Proper resource cleanup

## Security Testing

**Authentication Validation**:
- JWT token requirements
- User authorization checks
- Request header validation
- Cross-user data isolation

## Business Logic Validation

### Trip Status Management
- Initial trip status (active)
- End status values (completed, cancelled, etc.)
- Status transition validation

### Distance Calculation
- Trajectory distance tracking
- Trip metric computation
- HGAC (Houston-Galveston Area Council) flagging

### Calendar Integration
- Calendar event trip marking
- Work-related trip classification
- Time-based trip categorization

## Integration Points

**External Services**:
- Navigation app deep linking
- Location services integration
- Calendar system connectivity

**Internal Services**:
- User management system
- Reservation management
- Telework tracking system
- Notification services

## Quality Assurance

**Test Coverage Areas**:
- Happy path scenarios
- Edge case handling
- Error condition responses
- Data integrity validation
- Performance under load

**Validation Depth**:
- Field-level data validation
- Relationship integrity checks
- Business rule enforcement
- State consistency verification

This comprehensive test suite ensures the reliability and robustness of the core trip management functionality, providing confidence in the transportation service's ability to handle user journeys accurately and efficiently.