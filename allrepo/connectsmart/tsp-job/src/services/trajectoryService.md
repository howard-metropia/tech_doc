# Trajectory Service

## Overview

The Trajectory Service provides advanced GPS trajectory analysis and carpool validation functionality. It implements sophisticated algorithms for matching rider and driver GPS tracks to verify legitimate carpool trips, calculate proximity scores, and automate validation decisions for the duo carpool system.

## Service Information

- **Service Name**: Trajectory Service
- **File Path**: `/src/services/trajectoryService.js`
- **Type**: GPS Analysis & Validation Service
- **Dependencies**: TrajectoryDao, Geospatial Calculations, MySQL Database

## Core Functions

### setDao(dao)

Dependency injection function to set the data access object for trajectory operations.

**Purpose**: Configures data access layer for service operations
**Parameters**:
- `dao` (object): Data access object implementing trajectory queries
**Returns**: void

**Usage Pattern**:
```javascript
const trajectoryService = require('@app/src/services/trajectoryService');
const trajectoryDao = require('@app/src/services/trajectoryDao');

trajectoryService.setDao(trajectoryDao);
```

### calcDistance(lat1, lng1, lat2, lng2)

Calculates the great circle distance between two GPS coordinates using the Haversine formula.

**Purpose**: Computes accurate distance between GPS points for proximity analysis
**Parameters**:
- `lat1` (number): Latitude of first point in decimal degrees
- `lng1` (number): Longitude of first point in decimal degrees
- `lat2` (number): Latitude of second point in decimal degrees
- `lng2` (number): Longitude of second point in decimal degrees
**Returns**: Distance in meters (number)

**Mathematical Implementation**:
```javascript
const EARTH_RADIUS = 6378.137; // kilometers
const radLat1 = (lat1 * Math.PI) / 180.0;
const radLat2 = (lat2 * Math.PI) / 180.0;
const radLng1 = (lng1 * Math.PI) / 180.0;
const radLng2 = (lng2 * Math.PI) / 180.0;
const a = radLat1 - radLat2;
const b = radLng1 - radLng2;
let s = 2 * Math.asin(
  Math.sqrt(
    Math.pow(Math.sin(a / 2), 2) +
    Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2)
  )
);
s = s * EARTH_RADIUS * 1000; // Convert to meters
```

**Usage Example**:
```javascript
const distance = calcDistance(29.7604, -95.3698, 29.7749, -95.3659);
console.log(`Distance: ${distance.toFixed(2)} meters`);
// Output: Distance: 1643.50 meters
```

### fetchTrajectories(userId, tripId, startTimestamp, endTimestamp)

Retrieves and processes GPS trajectory data into time-segmented groups for analysis.

**Purpose**: Organizes raw GPS data into 5-second intervals for efficient comparison
**Parameters**:
- `userId` (string): User identifier
- `tripId` (number): Trip identifier
- `startTimestamp` (number): Start time in Unix timestamp
- `endTimestamp` (number): End time in Unix timestamp
**Returns**: Promise resolving to 2D array of trajectory segments

**Data Processing Logic**:
1. **Raw Data Retrieval**: Fetches trajectory documents from database
2. **Point Extraction**: Flattens trajectory arrays from multiple documents
3. **Time Segmentation**: Groups points into 5-second intervals
4. **Index Calculation**: `Math.floor((timestamp - startTimestamp) / 5)`
5. **Data Filtering**: Only includes points after start timestamp

**Output Structure**:
```javascript
[
  // Index 0: 0-5 seconds
  [
    { latitude: 29.7604, longitude: -95.3698, speed: 25.5 },
    { latitude: 29.7605, longitude: -95.3699, speed: 26.2 }
  ],
  // Index 1: 5-10 seconds  
  [
    { latitude: 29.7606, longitude: -95.3700, speed: 24.8 }
  ],
  // ... more time segments
]
```

**Example Usage**:
```javascript
const trajectories = await fetchTrajectories("123", 456, 1640995200, 1640998800);
console.log(`Processed ${trajectories.length} time segments`);
trajectories.forEach((segment, index) => {
  console.log(`Segment ${index}: ${segment.length} GPS points`);
});
```

### verifyTrajectoryGroup(driver, rider)

Analyzes a single time segment to determine if driver and rider were in close proximity.

**Purpose**: Validates carpool legitimacy by checking GPS proximity within time segment
**Parameters**:
- `driver` (array): Array of driver GPS points in time segment
- `rider` (array): Array of rider GPS points in time segment
**Returns**: Promise resolving to validation score (0 or 1)

**Validation Logic**:
```javascript
for (d of driver) {
  for (r of rider) {
    const distance = calcDistance(d.latitude, d.longitude, r.latitude, r.longitude);
    if (distance <= 100 && d.speed > 0 && r.speed > 0) {
      return 1; // Match found
    }
  }
}
return 0; // No match found
```

**Proximity Criteria**:
- **Distance Threshold**: 100 meters maximum separation
- **Speed Requirement**: Both participants must be moving (speed > 0)
- **Any Match Principle**: Single proximity match validates entire segment

**Usage Example**:
```javascript
const driverPoints = [
  { latitude: 29.7604, longitude: -95.3698, speed: 25.5 }
];
const riderPoints = [
  { latitude: 29.7605, longitude: -95.3699, speed: 24.8 }
];

const score = await verifyTrajectoryGroup(driverPoints, riderPoints);
console.log(`Segment validation score: ${score}`);
```

### verifyTrajectoryMatch(params)

Performs comprehensive trajectory matching analysis across entire trip duration.

**Purpose**: Calculates overall carpool validation score based on trajectory comparison
**Parameters** (destructured object):
- `driverId` (string): Driver user identifier
- `riderId` (string): Rider user identifier  
- `driverTripId` (number): Driver trip identifier
- `riderTripId` (number): Rider trip identifier
- `startTimeStamp` (number): Validation start time
- `endTimeStamp` (number): Validation end time
**Returns**: Promise resolving to cumulative validation score

**Analysis Process**:
1. **Data Retrieval**: Fetch trajectories for both participants
2. **Time Alignment**: Find common time segments between trajectories
3. **Segment Analysis**: Validate each overlapping time segment
4. **Score Accumulation**: Sum validation scores with maximum limit
5. **Early Termination**: Stop analysis at score threshold (36)

**Scoring Logic**:
```javascript
const keys = driverKeys.reduce((pre, cur) => {
  let match = false;
  riderKeys.forEach(k => {
    if (k === cur) match = true;
  });
  if (match) pre.push(cur);
  return pre;
}, []);

return keys.sort().reduce(async (pre, cur) => {
  pre = await pre;
  if (pre < 36) {
    pre += await verifyTrajectoryGroup(driverTrajectories[cur], riderTrajectories[cur]);
  }
  return pre;
}, 0);
```

**Performance Optimization**:
- **Maximum Score**: Analysis stops at score 36 for efficiency
- **Sequential Processing**: Processes segments sequentially to allow early termination
- **Time Intersection**: Only analyzes overlapping time periods

**Example Usage**:
```javascript
const score = await verifyTrajectoryMatch({
  driverId: "123",
  riderId: "456", 
  driverTripId: 789,
  riderTripId: 790,
  startTimeStamp: 1640995200,
  endTimeStamp: 1640998800
});

console.log(`Overall trajectory match score: ${score}`);
if (score > 35) {
  console.log("Carpool validation PASSED");
} else {
  console.log("Carpool validation FAILED");
}
```

### carpoolBlockValidationJob()

Automated job function that processes unvalidated carpool trips and performs trajectory analysis.

**Purpose**: Batch processes pending carpool validations using trajectory analysis
**Parameters**: None
**Returns**: Promise (async function)

**Job Processing Flow**:
1. **Date Calculation**: Determines yesterday's date for trip filtering
2. **Trip Retrieval**: Gets unvalidated driver trips from database
3. **Match Finding**: Locates corresponding rider trips for each driver
4. **Validation Execution**: Performs trajectory matching analysis
5. **Result Storage**: Saves validation results to database

**Validation Thresholds**:
- **Pass Threshold**: Score > 35 results in validation success
- **Fail Threshold**: Score ≤ 35 results in validation failure
- **Pass Status**: `validation_status: 2, passed: 1, score: 100`
- **Fail Status**: `validation_status: 1, passed: 0, score: actual_score`

**Date Handling**:
```javascript
const yesterday = new Date(new Date().getTime() - 1000 * 24 * 60 * 60)
  .toISOString()
  .replace('T', ' ')
  .split('.')[0];
```

**Processing Example**:
```javascript
await carpoolBlockValidationJob();
// Logs: "[carpoolBlockValidationJob] driverTripId: 789, riderTripId: 790, score: 42"
// Result: Validation passed with score 100 stored in database
```

**Error Handling**:
- **Continue on Error**: Individual trip failures don't stop batch processing
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Database Safety**: Atomic operations for validation result storage

## Validation Algorithm

### Time Segmentation Strategy
The service uses 5-second intervals to create manageable comparison units:

```javascript
// Time segment calculation
const segmentIndex = Math.floor((trajectory.timestamp - startTimestamp) / 5);
if (segmentIndex >= 0) {
  if (!trajectories[segmentIndex]) trajectories[segmentIndex] = [];
  trajectories[segmentIndex].push({
    latitude: trajectory.latitude,
    longitude: trajectory.longitude, 
    speed: trajectory.speed
  });
}
```

### Proximity Detection
Each segment uses distance calculation with specific thresholds:

- **Distance Limit**: 100 meters maximum separation
- **Speed Filter**: Both participants must be moving
- **Boolean Result**: Each segment scores 0 or 1

### Scoring System
The cumulative scoring system provides validation confidence:

- **Range**: 0 to theoretical maximum (number of time segments)
- **Threshold**: 35+ indicates successful carpool validation
- **Efficiency**: Analysis stops at 36 for performance
- **Pass Score**: Successful validations record score 100

## Integration with Carpool System

### Database Integration
The service integrates with the duo carpool database schema:

**Input Tables**:
- `trip`: Driver trip records with role = 1
- `duo_trip`: Pickup and dropoff timing data
- `duo_reservation`: Carpool offer matching data

**Output Table**:
- `duo_validated_result`: Validation results and scores

### Job Scheduling
The validation job is typically scheduled to run:
- **Frequency**: Daily execution for previous day's trips
- **Timing**: Off-peak hours to minimize database load
- **Scope**: Only unvalidated or incomplete validations

### Payment Integration
Validation results trigger payment processing:
- **Passed Validations**: Enable payment to driver
- **Failed Validations**: Prevent fraudulent payments
- **Score Storage**: Provides audit trail for disputes

## Performance Considerations

### Computational Complexity
- **Time Complexity**: O(n × m) where n and m are trajectory point counts
- **Early Termination**: Reduces average processing time
- **Segment Limits**: 5-second intervals prevent excessive comparisons

### Memory Management
```javascript
// Efficient trajectory processing
const processTrajectories = async (trajectories) => {
  // Process one segment at a time to manage memory
  for (const [index, segment] of trajectories.entries()) {
    if (segment && segment.length > 0) {
      await processSegment(segment, index);
    }
  }
};
```

### Database Optimization
- **Indexed Queries**: Efficient retrieval of trajectory data
- **Batch Processing**: Multiple trips processed in single job run
- **Connection Pooling**: Efficient database resource usage

## Error Handling & Resilience

### Data Validation
```javascript
const validateTrajectoryData = (trajectory) => {
  return trajectory.every(point => 
    typeof point.latitude === 'number' &&
    typeof point.longitude === 'number' &&
    typeof point.speed === 'number' &&
    point.latitude >= -90 && point.latitude <= 90 &&
    point.longitude >= -180 && point.longitude <= 180 &&
    point.speed >= 0
  );
};
```

### Exception Management
- **Graceful Degradation**: Continue processing other trips on individual failures
- **Comprehensive Logging**: Detailed error information for debugging
- **Data Integrity**: Ensures validation results are only written for valid data

### Job Resilience
```javascript
try {
  const score = await verifyTrajectoryMatch(params);
  await dao.writeDuoValidatedResult(validationData);
  logger.info(`Validation completed: score ${score}`);
} catch (error) {
  logger.error(`Validation failed for trip ${tripId}:`, error.message);
  // Continue with next trip
}
```

## Security Considerations

### Data Access Control
- **User Isolation**: Trajectory data filtered by user ownership
- **Trip Validation**: Verify user permissions for requested trips
- **Secure Calculations**: Prevent manipulation of validation scores

### Validation Integrity
- **Deterministic Results**: Same input always produces same output
- **Audit Trail**: Complete logging of validation decisions
- **Tamper Resistance**: Validation logic protected from manipulation

## Testing Strategies

### Unit Testing
```javascript
describe('Trajectory Service', () => {
  test('calcDistance returns accurate results', () => {
    const distance = calcDistance(0, 0, 0, 1);
    expect(distance).toBeCloseTo(111319.5, 1); // 1 degree longitude at equator
  });

  test('verifyTrajectoryGroup detects proximity', async () => {
    const driver = [{ latitude: 29.7604, longitude: -95.3698, speed: 25 }];
    const rider = [{ latitude: 29.7605, longitude: -95.3699, speed: 24 }];
    const score = await verifyTrajectoryGroup(driver, rider);
    expect(score).toBe(1);
  });
});
```

### Integration Testing
- **Database Connectivity**: Test trajectory data retrieval
- **End-to-End Validation**: Complete validation workflow testing
- **Performance Testing**: Measure processing time for large datasets
- **Error Scenarios**: Test handling of missing or invalid data

## Configuration & Deployment

### Environment Variables
- **Database Connections**: MongoDB and MySQL connection strings
- **Processing Limits**: Configurable thresholds and timeouts
- **Logging Levels**: Debug vs production logging configuration

### Monitoring & Alerting
```javascript
const validationMetrics = {
  processedTrips: 0,
  passedValidations: 0,
  failedValidations: 0,
  errors: 0,
  averageScore: 0
};

// Track metrics during job execution
logger.info(`Validation metrics:`, validationMetrics);
```

## Dependencies

- **TrajectoryDao**: Data access layer for trajectory and trip data
- **@maas/core/log**: Centralized logging system
- **Database Models**: TripTrajectory (MongoDB), Trip/DuoTrip (MySQL)
- **Mathematical Libraries**: Built-in Math functions for geospatial calculations