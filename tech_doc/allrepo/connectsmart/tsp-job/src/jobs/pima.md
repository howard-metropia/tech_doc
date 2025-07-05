# pima.js

## Overview
Job for synchronizing transportation data with PIMA (Pima Association of Governments) systems. This job orchestrates the extraction, transformation, and loading of users, reservations, and trip data to support regional transportation planning and coordination in the Pima County/Tucson metropolitan area.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/pima.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function and configurable inputs

## Key Dependencies
- `moment-timezone` - Timezone-aware date/time operations for Houston timezone scheduling
- `@maas/core/log` - Structured logging utility for operation tracking
- `@app/src/services/pima` - PIMA-specific data services (writeUsers, writeReservations, writeTrips)

## Core Functions

### Data Synchronization Orchestration
Manages three critical data synchronization processes:
- **User Data Export**: Synchronizes user profiles and account information
- **Reservation Data Export**: Transfers reservation and booking data
- **Trip Data Export**: Exports completed trip and travel pattern data

### Timezone-Aware Scheduling
Implements Houston timezone-based scheduling logic:
- **Automatic Scheduling**: Executes daily at 00:00:00 Houston time (America/Chicago)
- **Manual Override**: Supports manual execution with custom date ranges
- **Time Zone Validation**: Prevents execution outside scheduled hours for automated runs

### Error Handling and Validation
Comprehensive error management across all data operations:
- **Individual Service Monitoring**: Tracks success/failure of each data export
- **Graceful Degradation**: Continues processing despite individual service failures
- **Comprehensive Logging**: Records detailed error information for troubleshooting

## Processing Flow

### 1. Input Parameter Processing
```javascript
fn: async (start, end) => {
  // Handle null/empty parameter conversion
  if (start === '') start = 'null';
  if (end === '') end = 'null';
  
  // Timezone validation for scheduled execution
  const currentTime = moment.utc().tz('America/Chicago');
  if (start === 'null' && currentTime.hour() !== 0) {
    logger.warn(`Now: ${currentTime} isn't at 00:00:00 in Houston timezone`);
    return;
  }
}
```

### 2. User Data Synchronization
```javascript
try {
  await writeUsers();
} catch (err) {
  logger.error(`writePimaUsers failed:${err.message}`);
  failed = true;
}
```

### 3. Reservation Data Synchronization
```javascript
try {
  await writeReservations(start, end);
} catch (err) {
  logger.error(`writePimaReservations failed:${err.message}`);
  failed = true;
}
```

### 4. Trip Data Synchronization
```javascript
try {
  await writeTrips(start, end);
} catch (err) {
  logger.error(`writePimaTrips failed:${err.message}`);
  failed = true;
}
```

### 5. Error Aggregation and Reporting
```javascript
if (failed) {
  throw new Error(`pima job failed, check the logs!`);
}
```

## Data Models

### Job Input Configuration
```javascript
{
  inputs: {
    start: String,    // Start date for data range (YYYY-MM-DD or 'null')
    end: String,      // End date for data range (YYYY-MM-DD or 'null')
  }
}
```

### Execution Modes
```javascript
// Automated daily execution
{
  start: 'null',      // Use previous log date as start
  end: 'null',        // Use current date as end
  execution_time: '00:00:00 America/Chicago'
}

// Manual execution with date range
{
  start: '2024-01-01',  // Specific start date
  end: '2024-01-31',    // Specific end date
  execution_time: 'any' // Can run at any time
}
```

### Service Response Structure
```javascript
// Each service (writeUsers, writeReservations, writeTrips) returns:
{
  success: boolean,
  recordsProcessed: number,
  errors: Array<string>,
  processingTime: number
}
```

## Business Logic

### Scheduling Logic
```javascript
// Houston timezone validation for automated runs
const currentTime = moment.utc().tz('America/Chicago');
if (start === 'null' && currentTime.hour() !== 0) {
  // Skip execution - not at scheduled time
  return;
}
```

### Parameter Handling
- **Null Parameters**: `'null'` indicates system should determine date range from logs
- **Empty Parameters**: Converted to `'null'` for consistency
- **Date Parameters**: Explicit date ranges for manual execution
- **Timezone Considerations**: All times processed in Houston timezone (America/Chicago)

### Error Accumulation
```javascript
let failed = false;

// Each service failure sets failed flag
try {
  await serviceOperation();
} catch (err) {
  failed = true;  // Mark overall job as failed
  // Continue processing other services
}

// Final error reporting
if (failed) {
  throw new Error(`pima job failed, check the logs!`);
}
```

## Data Synchronization Services

### User Data Service (writeUsers)
```javascript
await writeUsers();
// Synchronizes:
// - User profiles and demographics
// - Account status and preferences  
// - Authentication and authorization data
// - User geographic and mobility preferences
```

### Reservation Data Service (writeReservations)
```javascript
await writeReservations(start, end);
// Synchronizes:
// - Trip reservations and bookings
// - Service requests and scheduling
// - Cancellations and modifications
// - Reservation status and confirmations
```

### Trip Data Service (writeTrips)
```javascript
await writeTrips(start, end);
// Synchronizes:
// - Completed trip records
// - Travel patterns and routes
// - Trip validation and verification
// - Performance metrics and analytics
```

## Error Handling Patterns

### Service-Level Error Handling
```javascript
try {
  await writeUsers();
} catch (err) {
  logger.error(`writePimaUsers failed:${err.message}`);
  failed = true;  // Mark failure but continue processing
}
```

### Comprehensive Error Reporting
```javascript
// Individual service errors logged separately
logger.error(`writePimaUsers failed:${err.message}`);
logger.error(`writePimaReservations failed:${err.message}`);
logger.error(`writePimaTrips failed:${err.message}`);

// Overall job failure reported at end
if (failed) {
  throw new Error(`pima job failed, check the logs!`);
}
```

### Graceful Degradation
- **Continue on Error**: Individual service failures don't stop other services
- **Detailed Logging**: Each error logged with specific service context
- **Overall Status**: Job marked as failed if any service fails
- **Operator Notification**: Clear error message indicates log review needed

## Performance Considerations

### Sequential Processing
- **Service Order**: Users → Reservations → Trips (maintains referential integrity)
- **Resource Management**: Sequential execution prevents resource contention
- **Memory Efficiency**: Services process data in batches to manage memory usage

### Timezone Optimization
- **Single Timezone Calculation**: Houston time calculated once per execution
- **Efficient Time Comparison**: Simple hour comparison for scheduling validation
- **UTC Conversion**: Consistent timezone handling across services

### Date Range Processing
- **Incremental Processing**: Uses log-based date ranges for efficiency
- **Manual Override**: Supports full reprocessing when needed
- **Boundary Handling**: Proper handling of date range boundaries

## Integration Points

### PIMA Government Systems
- **Data Format Compliance**: Ensures data meets PIMA format requirements
- **API Integration**: Interfaces with PIMA data collection systems
- **Validation Standards**: Meets government data quality standards

### Regional Transportation Planning
- **MPO Integration**: Supports Metropolitan Planning Organization requirements
- **Federal Reporting**: Enables compliance with federal transportation reporting
- **Regional Analytics**: Provides data for regional transportation analysis

### Internal System Coordination
- **Database Synchronization**: Coordinates with internal transportation databases
- **Service Dependencies**: Manages dependencies between user, reservation, and trip data
- **Data Consistency**: Ensures referential integrity across synchronized datasets

## Monitoring and Logging

### Service-Specific Logging
```javascript
logger.error(`writePimaUsers failed:${err.message}`);
logger.error(`writePimaReservations failed:${err.message}`);
logger.error(`writePimaTrips failed:${err.message}`);
```

### Schedule Validation Logging
```javascript
logger.warn(`Now: ${currentTime} isn't at 00:00:00 in Houston timezone`);
```

### Operation Status Tracking
```javascript
// Success/failure tracking for each service
// Overall job status determination
// Processing time and record count tracking
```

## Usage Scenarios

### Daily Automated Synchronization
- **Schedule**: Daily at midnight Houston time
- **Data Range**: Previous day's data based on logs
- **Purpose**: Regular government reporting compliance
- **Monitoring**: Automated failure alerting

### Manual Data Recovery
- **Trigger**: Manual execution with specific date ranges
- **Data Range**: Custom start/end dates
- **Purpose**: Recovery from synchronization failures
- **Validation**: Full data integrity checking

### Historical Data Export
- **Schedule**: On-demand execution
- **Data Range**: Extended historical periods
- **Purpose**: Research and analysis support
- **Performance**: Optimized for large dataset processing

## Configuration Dependencies

### Timezone Configuration
- **Primary Timezone**: America/Chicago (Houston time)
- **Execution Window**: 00:00:00 daily for automated runs
- **Manual Override**: No timezone restrictions for manual execution

### Service Configuration
- **PIMA Service Endpoints**: Configured in PIMA service module
- **Database Connections**: Portal database for source data
- **Log Management**: Previous execution tracking for incremental processing

### Government Compliance
- **Data Format Standards**: PIMA-specified data formats
- **Security Requirements**: Government-grade security protocols
- **Audit Trail**: Comprehensive logging for compliance auditing

## Notes
- **Government Integration**: Designed specifically for government data reporting requirements
- **Regional Transportation**: Supports Pima County/Tucson metropolitan area transportation planning
- **Compliance-Focused**: Ensures data quality and format compliance for government systems
- **Operational Reliability**: Robust error handling ensures data synchronization continuity
- **Houston Timezone**: Specifically configured for Houston-based operations scheduling
- **Scalable Architecture**: Designed to handle growing transportation data volumes efficiently