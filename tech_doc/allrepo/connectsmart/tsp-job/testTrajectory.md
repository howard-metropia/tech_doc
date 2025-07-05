# TSP Job Test: Trajectory Validation Service Test Documentation

## Quick Summary

**Purpose**: Integration test suite for carpool trajectory validation system implementing MET-13192 requirements for validating shared ride authenticity through GPS trajectory analysis.

**Key Features**:
- Tests carpool block validation job (`carpoolBlockValidationJob`)
- Validates trajectory-based carpool verification logic
- Implements mock DAO pattern for testing database interactions
- Covers both successful validation and failure scenarios
- Ensures proper scoring and validation status assignment

**Technology Stack**: Mocha testing framework, Chai assertions, custom DAO mocking

## Technical Analysis

### Code Structure

The test file implements a comprehensive integration testing framework for trajectory validation:

```javascript
const service = require('@app/src/services/trajectoryService');
const expect = require('chai').expect;
```

### Key Components

**Mock DAO Architecture**:
The test implements a complete Data Access Object (DAO) mock that simulates database operations:

```javascript
dao = {
  localStorage: [],  // In-memory storage for test results
  getTrajectories: async (userId, tripId, startTimestamp, endTimestamp) => {
    // Generate mock trajectory data
  },
  getTrips: async yesterday => {
    // Return mock trip data
  },
  getReservations: async reservationId => {
    // Return mock reservation data  
  },
  writeDuoValidatedResult: async function(data) {
    // Store validation results
  }
};
```

**Trajectory Data Generation**:
- **Success Case**: Generates full trajectory covering entire time window
- **Failure Case**: Generates limited trajectory (5-minute window only)
- Uses linear progression for latitude/longitude coordinates
- Maintains consistent speed and timestamp intervals

**Validation Logic Testing**:
- Tests driver-passenger relationship validation
- Verifies trajectory overlap calculation algorithms  
- Validates scoring mechanisms (0-100 scale)
- Ensures proper pass/fail determination

### Implementation Details

**Trip Data Structure**:
```javascript
const mockTrip = {
  id: 1,
  reservation_id: 1,
  started_on: '2023-01-01 12:00:00',  // 1 hour ago
  ended_on: null,
  passenger_id: 1,
  pick_up_time: '2023-01-01 12:00:00',
  drop_off_time: 1,
  status: 8,  // Completed status
  passenger_trip_id: null,
  passed: null,
  score: null
};
```

**Reservation Mapping**:
```javascript
const mockReservation = {
  driver_trip_id: 1,
  rider_trip_id: 2,
  driver_user_id: 1,
  rider_user_id: 2
};
```

**Trajectory Point Structure**:
```javascript
const trajectoryPoint = {
  latitude: 0.01 + (timestamp - startTimestamp) * 0.01 / 10,
  longitude: 0.01 + (timestamp - startTimestamp) * 0.01 / 10,
  speed: 30,  // Consistent speed
  timestamp: timestamp
};
```

**Validation Result Format**:
```javascript
const validationResult = {
  driver_trip_id: 1,
  passenger_trip_id: 2,
  passed: 1,  // 1 = passed, 0 = failed
  score: 100, // 0-100 scale
  validation_status: 1  // Processing status
};
```

## Usage/Integration

### Test Execution

**Running Trajectory Tests**:
```bash
# Run trajectory validation tests
npm test test/testTrajectory.js

# Run with detailed output
npm test test/testTrajectory.js --verbose
```

**Service Integration**:
```javascript
// Inject mock DAO for testing
service.setDao(dao);

// Execute validation job
await service.carpoolBlockValidationJob();

// Retrieve results from mock storage
const result = dao.localStorage[0];
```

### Integration Points

**Service Dependencies**:
- `@app/src/services/trajectoryService`: Core validation service
- Trajectory data access layer
- Trip and reservation management systems
- Validation result storage mechanisms

**Database Integration**:
- Reads from trip and reservation tables
- Accesses trajectory data collections
- Writes validation results to duo_validated_result table
- Maintains audit trail for validation decisions

### Validation Algorithm

**Success Criteria**:
- Complete trajectory coverage during trip window
- Sufficient data points for analysis
- Geographic proximity validation
- Temporal overlap verification

**Failure Conditions**:
- Insufficient trajectory data
- Geographic divergence between trajectories
- Temporal misalignment
- Data quality issues

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with expect interface
- `mocha`: Test runner framework (implicit)

**Service Layer**:
- `@app/src/services/trajectoryService`: Core trajectory validation service
- Custom DAO abstraction layer for database operations

### Business Logic Dependencies

**Data Sources**:
- Trip management system
- Reservation/booking system  
- GPS trajectory collection service
- User management system

**Validation Engine**:
- Geographic distance calculation algorithms
- Temporal alignment analysis
- Statistical correlation methods
- Scoring and threshold determination

### External Integrations

**GPS Data Sources**:
- Mobile device trajectory collection
- Real-time location tracking
- Offline trajectory synchronization
- Data quality validation

## Code Examples

### Basic Test Structure

```javascript
describe('integration tests for new trajectory calc implementation for MET-13192', () => {
  describe('normal success case', () => {
    let dao;
    
    before(async () => {
      dao = {
        localStorage: [],
        getTrajectories: async (userId, tripId, startTimestamp, endTimestamp) => {
          const trajectory = [];
          // Generate trajectory for full time window
          for (let i = startTimestamp; i < endTimestamp; i++) {
            trajectory.push({
              latitude: 0.01 + (i - startTimestamp) * 0.01 / 10,
              longitude: 0.01 + (i - startTimestamp) * 0.01 / 10,
              speed: 30,
              timestamp: i,
            });
          }
          return [{
            user_id: userId,
            trip_id: tripId,
            timestamp: endTimestamp,
            trajectory,
          }];
        },
        // ... other DAO methods
      };
    });

    it('test success result', async () => {
      service.setDao(dao);
      await service.carpoolBlockValidationJob();
      
      const result = dao.localStorage[0];
      expect(result.driver_trip_id).to.eq(1);
      expect(result.passenger_trip_id).to.eq(2);
      expect(result.passed).to.eq(1);
      expect(result.score).to.eq(100);
    });
  });
});
```

### Mock Trip Data Setup

```javascript
getTrips: async yesterday => {
  return [{
    id: 1,
    reservation_id: 1,
    started_on: new Date(new Date().getTime() - 1000 * 60 * 60)
      .toISOString().replace('T', ' ').split('.')[0],
    ended_on: null,
    passenger_id: 1,
    pick_up_time: new Date(new Date().getTime() - 1000 * 60 * 60)
      .toISOString().replace('T', ' ').split('.')[0],
    drop_off_time: 1,
    status: 8,  // Completed status
    passenger_trip_id: null,
    passed: null,
    score: null,
  }];
}
```

### Trajectory Generation Pattern

```javascript
getTrajectories: async (userId, tripId, startTimestamp, endTimestamp) => {
  const trajectory = [];
  
  // Success case: Full trajectory coverage
  for (let i = startTimestamp; i < endTimestamp; i++) {
    trajectory.push({
      latitude: 0.01 + (i - startTimestamp) * 0.01 / 10,
      longitude: 0.01 + (i - startTimestamp) * 0.01 / 10,
      speed: 30,
      timestamp: i,
    });
  }
  
  // Failure case: Limited trajectory (only 5 minutes)  
  for (let i = startTimestamp; i < startTimestamp + 5 * 10; i++) {
    trajectory.push({
      latitude: 0.01 + (i - startTimestamp) * 0.01 / 10,
      longitude: 0.01 + (i - startTimestamp) * 0.01 / 10,
      speed: 30,
      timestamp: i,
    });
  }
  
  return [{
    user_id: userId,
    trip_id: tripId,
    timestamp: endTimestamp,
    trajectory,
  }];
}
```

### Validation Result Storage

```javascript
writeDuoValidatedResult: async function(data) {
  this.localStorage.push(data);
}

// Test validation
it('test failed result', async () => {
  service.setDao(dao);
  await service.carpoolBlockValidationJob();
  
  expect(dao.localStorage.length).to.eq(1);
  expect(dao.localStorage[0].passed).to.eq(0);
  expect(dao.localStorage[0].validation_status).to.eq(1);
});
```

### Reservation Mapping

```javascript
getReservations: async reservationId => {
  return [{
    driver_trip_id: 1,
    rider_trip_id: 2,
    driver_user_id: 1,
    rider_user_id: 2,
  }];
}
```

This comprehensive test suite ensures the trajectory validation system correctly identifies authentic carpool trips through GPS analysis, providing robust fraud detection capabilities while maintaining high accuracy standards for legitimate shared rides.