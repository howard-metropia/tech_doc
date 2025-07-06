# analytic-database.js

## Overview
Comprehensive ETL (Extract, Transform, Load) job that processes and transfers data from operational databases to analytics databases. This job orchestrates multiple data pipeline components for business intelligence and reporting purposes.

## Purpose
- Process and transfer operational data to analytics databases
- Coordinate multiple ETL operations with error handling
- Support both scheduled and manual execution modes
- Maintain data consistency across analytics pipelines

## Key Features
- **Multi-Component ETL**: Orchestrates user, trip, activity, and transaction data processing
- **Time Zone Handling**: Supports Houston timezone scheduling (00:00:00 execution)
- **Error Resilience**: Individual component error isolation with comprehensive logging
- **Manual Override**: Special handling for manual script execution (MET mode)
- **QuickSight Integration**: Includes AWS QuickSight ETL processing

## Dependencies
```javascript
const moment = require('moment-timezone');
const { logger } = require('@maas/core/log');
const { writeDBTrip, manuallyScript } = require('@app/src/services/dbTrips');
const { writeDBUser, setUserTimezone } = require('@app/src/services/dbUsers');
const writeDBAppActivity = require('@app/src/services/dbAppActivity');
const writeTicketTransaction = require('@app/src/services/ticket_transaction');
const writeCoinTransaction = require('@app/src/services/coin_transaction');
const { quickSightEtl } = require('@app/src/services/quick-sight-etl');
```

## Input Parameters
```javascript
inputs: {
  start: String,  // Start date for data processing
  end: String,    // End date for data processing
}
```

### Parameter Handling
- `start === 'met'`: Triggers manual script mode with `end` as script parameter
- `start === 'null'`: Uses automatic date detection from previous logs
- Empty strings converted to 'null' for automatic processing

## Core Processing Pipeline

### 1. Execution Mode Detection
```javascript
if (start.toLowerCase() === 'met') {
  await manuallyScript(end);
  return;
}
```

### 2. Timezone Validation
```javascript
const currentTime = moment.utc().tz('America/Chicago');
if (start === 'null' && currentTime.hour() !== 0) {
  logger.warn(`Now: ${currentTime} isn't at 00:00:00 in Houston timezone`);
  return;
}
```

### 3. Data Processing Sequence
```javascript
// User timezone setup
await setUserTimezone();

// User data ETL
await writeDBUser();

// Trip data ETL
await writeDBTrip(start, end);

// App activity data ETL
await writeDBAppActivity(start, end);

// Transaction data ETL
await writeTicketTransaction(start, end);
await writeCoinTransaction(start, end);

// QuickSight analytics ETL
await quickSightEtl();
```

## ETL Components

### User Data Processing
- **setUserTimezone()**: Updates user timezone information
- **writeDBUser()**: Transfers user data to analytics database
- User profile and registration data processing

### Trip Data Processing
- **writeDBTrip(start, end)**: Processes trip data within date range
- Trip origin, destination, and routing information
- Travel mode and duration analytics

### Activity Data Processing
- **writeDBAppActivity(start, end)**: App usage and interaction data
- User engagement metrics and behavior patterns
- Feature usage analytics

### Transaction Processing
- **writeTicketTransaction(start, end)**: Transit ticket purchase data
- **writeCoinTransaction(start, end)**: Point and reward transaction data
- Payment and incentive analytics

### QuickSight Integration
- **quickSightEtl()**: AWS QuickSight data preparation
- Business intelligence dashboard data
- Visualization-ready data formatting

## Error Handling Strategy

### Individual Component Isolation
```javascript
let failed = false;
try {
  await writeDBUser();
} catch (err) {
  logger.error(`writeDBUser failed:${err.message}`);
  failed = true;
}
```

### Comprehensive Error Tracking
- Each ETL component errors are logged individually
- Process continues despite individual component failures
- Final error aggregation and reporting

### Failure Reporting
```javascript
if (failed) {
  throw new Error(`analytic-database job failed, check the logs!`);
}
```

## Scheduling Logic

### Automatic Execution
- Validates execution time is 00:00:00 Houston timezone
- Prevents duplicate executions during incorrect timing
- Supports daily scheduled processing

### Manual Execution
- Bypasses time validation for manual runs
- Supports custom date range processing
- Special MET mode for maintenance scripts

## Data Flow Architecture

### Source Systems
- Operational user database
- Trip tracking system
- App activity logs
- Transaction processing systems

### Target Systems
- Analytics database
- Business intelligence warehouse
- AWS QuickSight data sources
- Reporting data marts

## Performance Considerations

### Sequential Processing
- Components run sequentially to manage resource usage
- Individual error isolation prevents cascade failures
- Progress tracking through comprehensive logging

### Resource Management
- Memory-efficient data streaming where possible
- Database connection pooling through service layer
- Proper cleanup and resource disposal

## Monitoring and Alerting

### Success Tracking
- Component-level execution logging
- Processing time and volume metrics
- Data quality validation results

### Failure Detection
- Individual component error reporting
- Aggregated failure status
- Comprehensive error message logging

## Integration Points
- **Database Services**: Multiple ETL service integrations
- **Time Zone Services**: Houston timezone coordination
- **AWS QuickSight**: Cloud analytics integration
- **Logging System**: Comprehensive operation tracking

## Usage Patterns
- Daily scheduled execution at midnight Houston time
- Manual execution for data backfill operations
- Maintenance script execution through MET mode
- Error recovery and retry operations

## Business Value
- Enables business intelligence and reporting
- Supports data-driven decision making
- Provides real-time analytics capabilities
- Maintains data consistency across systems