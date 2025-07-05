# Trajectory Data Access Object (DAO)

## Overview

The Trajectory DAO provides data access layer functions for GPS trajectory analysis and carpool validation operations. It handles complex database queries across MySQL and MongoDB to support trip validation, carpool verification, and duo ride matching systems.

## Service Information

- **Service Name**: Trajectory DAO
- **File Path**: `/src/services/trajectoryDao.js`
- **Type**: Data Access Layer
- **Dependencies**: MongoDB (TripTrajectory), MySQL (Portal), Knex.js

## Core Functions

### getTrajectories(userId, tripId, startTimestamp, endTimestamp)

Retrieves GPS trajectory data from MongoDB for specific user and trip within time range.

**Purpose**: Fetches raw GPS tracking data for trajectory analysis and validation
**Parameters**:
- `userId` (string): User identifier (converted to string for MongoDB compatibility)
- `tripId` (number): Trip identifier
- `startTimestamp` (number): Start time in Unix timestamp
- `endTimestamp` (number): End time in Unix timestamp
**Returns**: Promise resolving to array of TripTrajectory documents

**MongoDB Query Structure**:
```javascript
{
  user_id: `${userId}`,           // String conversion required
  trip_id: tripId,
  $and: [
    { 'trajectory.timestamp': { $gte: startTimestamp } },
    { 'trajectory.timestamp': { $lte: endTimestamp } }
  ]
}
```

**Data Structure**:
Each trajectory document contains:
```javascript
{
  user_id: "123",
  trip_id: 456,
  trajectory: [
    {
      timestamp: 1640995200,
      latitude: 29.7604,
      longitude: -95.3698,
      speed: 25.5
    },
    // ... more trajectory points
  ]
}
```

**Usage Example**:
```javascript
const trajectories = await getTrajectories(
  "123", 
  456, 
  1640995200, 
  1640998800
);
console.log(`Found ${trajectories.length} trajectory records`);
```

### getTrips(yesterday)

Retrieves unvalidated driver trips from duo carpool system for validation processing.

**Purpose**: Identifies driver trips that need trajectory validation
**Parameters**:
- `yesterday` (string): Date string in 'YYYY-MM-DD HH:mm:ss' format
**Returns**: Promise resolving to array of trip records

**SQL Query Logic**:
```sql
SELECT t.id, t.reservation_id, t.started_on, t.ended_on, 
       dt.passenger_id, dt.pick_up_time, dt.drop_off_time, 
       dvr.passenger_trip_id, dvr.passed, dvr.score 
FROM trip t
INNER JOIN duo_trip dt ON dt.trip_id = t.id
LEFT JOIN duo_validated_result dvr ON dvr.driver_trip_id = t.id
WHERE t.role = 1 
  AND (dvr.id IS NULL OR dvr.validation_status < 2) 
  AND t.started_on >= ?
GROUP BY t.id
```

**Query Filters**:
- **Role = 1**: Only driver trips
- **Validation Status < 2**: Incomplete or failed validations
- **Started After**: Only recent trips from specified date
- **Group By**: Prevents duplicate records

**Result Structure**:
```javascript
[
  {
    id: 789,
    reservation_id: 101,
    started_on: "2024-01-01 08:00:00",
    ended_on: "2024-01-01 09:30:00", 
    passenger_id: 456,
    pick_up_time: "2024-01-01 08:15:00",
    drop_off_time: "2024-01-01 09:15:00",
    passenger_trip_id: 790,
    passed: null,
    score: null
  }
]
```

### getReservations(reservationId)

Retrieves matching driver and rider trip pairs for duo carpool validation.

**Purpose**: Finds connected trips in carpool arrangements for validation
**Parameters**:
- `reservationId` (number): Reservation identifier to find matches
**Returns**: Promise resolving to array of trip pair records

**SQL Query Logic**:
```sql
SELECT trip1.id as driver_trip_id, trip2.id as rider_trip_id, 
       trip1.user_id as driver_user_id, trip2.user_id as rider_user_id 
FROM duo_reservation dr1
JOIN duo_reservation dr2 ON dr2.offer_id = dr1.offer_id 
                        AND dr2.reservation_id <> dr1.reservation_id
JOIN trip as trip1 ON trip1.reservation_id = dr1.reservation_id
JOIN trip as trip2 ON trip2.reservation_id = dr2.reservation_id
WHERE dr1.reservation_id = ?
LIMIT 1
```

**Join Logic**:
1. **Self-Join**: duo_reservation table joined with itself
2. **Offer Matching**: Same offer_id but different reservation_id
3. **Trip Linking**: Each reservation linked to its trip record
4. **Single Result**: LIMIT 1 for primary match

**Result Structure**:
```javascript
[
  {
    driver_trip_id: 789,
    rider_trip_id: 790,
    driver_user_id: 123,
    rider_user_id: 456
  }
]
```

### writeDuoValidatedResult(data)

Writes or updates carpool validation results with schema compatibility checking.

**Purpose**: Stores trajectory validation results for carpool trips
**Parameters**:
- `data` (object): Validation result data including trip IDs and scores
**Returns**: Promise (async function)

**Schema Validation**:
```javascript
const hasValidationStatus = await knex.schema.hasColumn('duo_validated_result', 'validation_status');
const hasPaymentStatus = await knex.schema.hasColumn('duo_validated_result', 'payment_status');
```

**Data Structure**:
```javascript
{
  driver_trip_id: 789,
  passenger_trip_id: 790,
  passed: 1,                    // 1 = passed, 0 = failed
  score: 85,                    // Validation score (0-100)
  validation_status: 2,         // 1 = failed, 2 = passed
  payment_status: 0,            // Payment processing status
  created_on: "2024-01-01 10:00:00"
}
```

**Upsert Logic**:
1. **Existence Check**: Query for existing record by trip IDs
2. **Insert New**: Create record if none exists
3. **Update Existing**: Modify existing record, removing certain fields
4. **Error Handling**: Graceful degradation if schema incompatible

**Example Usage**:
```javascript
await writeDuoValidatedResult({
  driver_trip_id: 789,
  passenger_trip_id: 790,
  passed: 1,
  score: 95,
  validation_status: 2,
  created_on: new Date().toISOString().replace('T', ' ').split('.')[0]
});
```

## Data Models & Relationships

### TripTrajectory (MongoDB)
```javascript
{
  _id: ObjectId,
  user_id: String,              // Note: String type, not Number
  trip_id: Number,
  trajectory: [
    {
      timestamp: Number,        // Unix timestamp
      latitude: Number,         // GPS latitude
      longitude: Number,        // GPS longitude
      speed: Number            // Speed in units/hour
    }
  ],
  created_at: Date,
  updated_at: Date
}
```

### Trip (MySQL)
```sql
CREATE TABLE trip (
  id INT PRIMARY KEY,
  user_id INT,
  reservation_id INT,
  started_on DATETIME,
  ended_on DATETIME,
  role TINYINT,               -- 1 = driver, 0 = passenger
  -- ... other fields
);
```

### DuoTrip (MySQL)
```sql
CREATE TABLE duo_trip (
  id INT PRIMARY KEY,
  trip_id INT,
  passenger_id INT,
  pick_up_time DATETIME,
  drop_off_time DATETIME,
  -- ... other fields
);
```

### DuoValidatedResult (MySQL)
```sql
CREATE TABLE duo_validated_result (
  id INT PRIMARY KEY,
  driver_trip_id INT,
  passenger_trip_id INT,
  passed TINYINT,             -- 0 = failed, 1 = passed
  score INT,                  -- Validation score 0-100
  validation_status TINYINT,  -- 1 = failed, 2 = passed
  payment_status TINYINT,     -- Payment processing status
  created_on DATETIME,
  -- ... other fields
);
```

### DuoReservation (MySQL)
```sql
CREATE TABLE duo_reservation (
  id INT PRIMARY KEY,
  reservation_id INT,
  offer_id INT,               -- Links related reservations
  -- ... other fields
);
```

## Query Optimization

### MongoDB Queries
**Recommended Indexes**:
```javascript
// Compound index for trajectory queries
db.trip_trajectory.createIndex({
  "user_id": 1,
  "trip_id": 1,
  "trajectory.timestamp": 1
});

// Individual field indexes
db.trip_trajectory.createIndex({"user_id": 1});
db.trip_trajectory.createIndex({"trip_id": 1});
```

### MySQL Queries
**Recommended Indexes**:
```sql
-- Trip table indexes
CREATE INDEX idx_trip_role_started ON trip(role, started_on);
CREATE INDEX idx_trip_reservation ON trip(reservation_id);

-- Duo tables indexes  
CREATE INDEX idx_duo_trip_trip_id ON duo_trip(trip_id);
CREATE INDEX idx_duo_validated_driver ON duo_validated_result(driver_trip_id);
CREATE INDEX idx_duo_reservation_offer ON duo_reservation(offer_id);
```

## Error Handling & Logging

### Database Error Handling
```javascript
const { logger } = require('@maas/core/log');

// Example error handling pattern
try {
  const result = await getTrajectories(userId, tripId, start, end);
  logger.info(`Retrieved ${result.length} trajectory records`);
} catch (error) {
  logger.error(`Failed to get trajectories: ${error.message}`);
  throw error;
}
```

### Schema Compatibility
The `writeDuoValidatedResult` function includes schema checking:
```javascript
if (hasValidationStatus && hasPaymentStatus) {
  // Proceed with full functionality
} else {
  logger.info(`duo_validated_result table does not have validation_status or payment_status column.`);
  // Graceful degradation
}
```

## Integration Points

### Used By
- **TrajectoryService**: GPS trajectory analysis and validation
- **Carpool Validation Jobs**: Automated trip verification
- **Duo Carpool System**: Rider-driver matching validation
- **Payment Processing**: Validation-based payment triggers

### Database Dependencies
- **MongoDB**: TripTrajectory collection for GPS data
- **MySQL Portal**: Trip, reservation, and validation tables
- **Knex.js**: SQL query builder and connection management
- **@maas/core/mysql**: Database connection configuration

## Performance Considerations

### MongoDB Performance
- **Large Dataset Handling**: Trajectory data can be voluminous
- **Time Range Queries**: Efficient timestamp-based filtering
- **Index Utilization**: Compound indexes for multi-field queries
- **Document Size**: Trajectory arrays can grow large

### MySQL Performance  
- **Complex Joins**: Multiple table joins for duo carpool data
- **Date Filtering**: Efficient date range operations
- **Duplicate Prevention**: GROUP BY clauses prevent duplicates
- **Index Coverage**: Covering indexes for common query patterns

### Memory Management
```javascript
// Process large trajectory datasets in chunks
const processTrajectories = async (trajectories) => {
  for (const batch of chunkArray(trajectories, 100)) {
    await processBatch(batch);
    // Allow garbage collection between batches
  }
};
```

## Data Consistency

### Cross-Database Consistency
- **MongoDB → MySQL**: Trajectory validation results stored in MySQL
- **Referential Integrity**: Trip IDs must exist in both systems
- **Timestamp Alignment**: Consistent time representation across systems
- **Transaction Boundaries**: No cross-database transactions

### Data Validation
```javascript
// Validate trajectory data before processing
const validateTrajectoryData = (trajectory) => {
  return trajectory.every(point => 
    point.timestamp &&
    point.latitude >= -90 && point.latitude <= 90 &&
    point.longitude >= -180 && point.longitude <= 180 &&
    point.speed >= 0
  );
};
```

## Security Considerations

### Input Validation
- **User ID**: String conversion and validation
- **Trip ID**: Numeric validation
- **Timestamps**: Unix timestamp validation
- **SQL Injection**: Parameterized queries prevent injection

### Data Access Control
- **User Isolation**: Queries filtered by user_id
- **Trip Ownership**: Verify user owns requested trip data
- **Validation Results**: Secure storage of validation outcomes
- **Audit Trail**: Track data access and modifications

## Testing Strategies

### Unit Testing
```javascript
const trajectoryDao = require('@app/src/services/trajectoryDao');

describe('TrajectoryDao', () => {
  test('getTrajectories returns filtered data', async () => {
    const result = await trajectoryDao.getTrajectories(
      "123", 789, 1640995200, 1640998800
    );
    expect(Array.isArray(result)).toBe(true);
    expect(result[0]).toHaveProperty('trajectory');
  });
});
```

### Integration Testing
- **Database Connectivity**: Test MongoDB and MySQL connections
- **Query Performance**: Measure query execution times
- **Data Integrity**: Verify cross-database consistency
- **Schema Evolution**: Test compatibility with schema changes

## Migration Considerations

### Data Type Compatibility
- **User ID Types**: MongoDB uses string, MySQL uses integer
- **Timestamp Formats**: Unix timestamps vs MySQL DATETIME
- **Geospatial Data**: GPS coordinates precision handling
- **Score Ranges**: Validation score boundaries (0-100)

### Schema Evolution
```javascript
// Example migration check
const checkSchemaVersion = async () => {
  const hasNewColumn = await knex.schema.hasColumn('duo_validated_result', 'new_field');
  if (!hasNewColumn) {
    logger.warn('Schema migration required for new validation features');
  }
};
```

## Dependencies

- **TripTrajectory**: MongoDB model for GPS trajectory data
- **knex**: SQL query builder for MySQL operations
- **@maas/core/mysql**: MySQL connection management
- **@maas/core/log**: Centralized logging system