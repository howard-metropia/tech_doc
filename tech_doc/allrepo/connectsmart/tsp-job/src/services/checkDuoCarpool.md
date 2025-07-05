# TSP Job Service: checkDuoCarpool.js

## Quick Summary

The `checkDuoCarpool.js` service monitors and validates carpool trip scoring accuracy within the ConnectSmart platform. It identifies anomalous duo carpool validation results where both driver and passenger have trajectory data but received zero scores, calculates error ratios, and reports findings to InfluxDB for monitoring and alerting. This service ensures the quality and reliability of the carpool validation system.

## Technical Analysis

### Core Architecture

The service implements a comprehensive carpool validation monitoring system with the following components:

- **Time Period Management**: Generates 24-hour analysis windows with UTC alignment
- **Data Validation**: Identifies scoring anomalies in duo carpool results
- **Trajectory Verification**: Cross-references trip trajectories with validation scores
- **Metrics Collection**: Calculates error ratios and performance indicators
- **Monitoring Integration**: Reports findings to InfluxDB for alerting

### Key Functions

#### getPeriod()
Generates standardized time periods for analysis:
```javascript
const getPeriod = () => {
  const datetime = moment()
    .utc()
    .set({
      hour: 22,
      minute: 0,
      second: 0,
      millisecond: 0,
    })
    .utcOffset(0);
  const today = datetime.clone().subtract(1, 'second').toISOString();
  const yesterday = datetime.clone().subtract(1, 'day').toISOString();
  return [yesterday, today];
};
```

#### getDuoResultsByPeriod()
Retrieves carpool validation results for analysis:
```javascript
const getDuoResultsByPeriod = async (period) => {
  let results;
  try {
    results = await DuoValidatedResult.query()
      .select([
        'id',
        'score',
        'driver_trip_id',
        'passenger_trip_id',
        'created_on',
      ])
      .whereBetween('created_on', period);
  } catch (e) {
    const msg = {
      content: 'error occurred while querying the duo_validated_result',
      params: { period },
      err: e.message,
    };
    logger.error(msg);
  }
  return results ?? [];
};
```

#### getTrajectoryByTripId()
Fetches trip trajectory data from MongoDB:
```javascript
const getTrajectoryByTripId = async (idList) => {
  let results;
  try {
    results = await TripTrajectory.find({ trip_id: { $in: idList } });
  } catch (e) {
    const msg = {
      content: 'error occurred while querying the trip_trajectory',
      params: { id: idList },
    };
    logger.error(msg);
    return [];
  }
  return results;
};
```

#### getErrorRecords()
Identifies problematic validation results:
```javascript
const getErrorRecords = async (duoResultRecords) => {
  const errorRecordList = [];
  await Promise.all(
    duoResultRecords
      .filter((record) => record.score === 0) // Focus on zero scores
      .map(async (record) => {
        const tripTrajectory = await getTrajectoryByTripId([
          record.driver_trip_id,
          record.passenger_trip_id,
        ]);
        
        // Both have trajectory but score is 0 = anomaly
        if (tripTrajectory.length === 2) {
          errorRecordList.push({
            recordId: record.id,
            driverTripId: record.driver_trip_id,
            passengerTripId: record.passenger_trip_id,
            createdOn: record.created_on,
          });
        }
      }),
  );
  return errorRecordList;
};
```

### Monitoring and Metrics

#### Error Ratio Calculation
```javascript
const calcErrorRatio = (errorDuoRecordCount, totalDuoRecordCount) => {
  const ratio = totalDuoRecordCount === 0 ? 0 : errorDuoRecordCount / totalDuoRecordCount;
  return Number(ratio.toFixed(4));
};
```

#### InfluxDB Integration
Reports metrics for monitoring and alerting:
```javascript
const writeResultToInfluxDB = async (fields) => {
  const influxData = {
    measurement: 'duo_score_error',
    tags: ['duo_carpool'],
    fields,
  };
  await write(influxData, true);
};
```

### Data Models Integration

The service integrates with multiple data models:

- **DuoValidatedResult**: Carpool validation scores (SQL database)
- **TripTrajectory**: Trip trajectory data (MongoDB)

## Usage/Integration

### Scheduled Monitoring

The service is typically executed as a scheduled job for continuous monitoring:

```javascript
const { 
  getPeriod, 
  getDuoResultsByPeriod, 
  getErrorRecords, 
  calcErrorRatio,
  writeResultToInfluxDB 
} = require('./checkDuoCarpool');

// Daily carpool validation check
async function runDuoCarpoolCheck() {
  const [yesterday, today] = getPeriod();
  
  // Get validation results for the period
  const duoResults = await getDuoResultsByPeriod([yesterday, today]);
  
  // Identify error records
  const errorRecords = await getErrorRecords(duoResults);
  
  // Calculate metrics
  const errorRatio = calcErrorRatio(errorRecords.length, duoResults.length);
  
  // Report to monitoring system
  await writeResultToInfluxDB({
    total_records: duoResults.length,
    error_records: errorRecords.length,
    error_ratio: errorRatio,
  });
  
  return {
    period: [yesterday, today],
    totalRecords: duoResults.length,
    errorRecords: errorRecords.length,
    errorRatio: errorRatio,
  };
}
```

### Error Detection Logic

The service identifies three types of validation scenarios:

1. **Normal**: Both trips have trajectories and valid scores (>0)
2. **Expected Zero**: One or both trips lack trajectory data (score = 0 expected)
3. **Anomalous**: Both trips have trajectories but score = 0 (error condition)

### Integration with Alerting Systems

Results are written to InfluxDB for monitoring dashboards and alerts:
```javascript
// InfluxDB data structure
{
  measurement: 'duo_score_error',
  tags: ['duo_carpool'],
  fields: {
    total_records: 150,
    error_records: 3,
    error_ratio: 0.0200,
    timestamp: '2023-12-01T22:00:00Z'
  }
}
```

## Dependencies

### External Packages
- `moment`: Date/time manipulation for period calculations
- `@maas/core/log`: Centralized logging system

### Internal Services
- `@app/src/models/DuoValidatedResult`: Carpool validation results model
- `@app/src/models/TripTrajectory`: Trip trajectory data model
- `@app/src/helpers/influxDb`: InfluxDB integration for metrics

### Database Dependencies
- **MySQL**: duo_validated_result table for validation scores
- **MongoDB**: trip_trajectory collection for trajectory data
- **InfluxDB**: Time-series database for monitoring metrics

## Code Examples

### Daily Validation Check
```javascript
const checkDuoCarpool = require('./checkDuoCarpool');

// Generate analysis period (yesterday 22:00 to today 22:00 UTC)
const [startTime, endTime] = checkDuoCarpool.getPeriod();
console.log(`Analyzing period: ${startTime} to ${endTime}`);

// Get all duo results for the period
const duoResults = await checkDuoCarpool.getDuoResultsByPeriod([startTime, endTime]);
console.log(`Found ${duoResults.length} duo validation results`);

// Identify problematic records
const errorRecords = await checkDuoCarpool.getErrorRecords(duoResults);
console.log(`Found ${errorRecords.length} error records`);

// Calculate error ratio
const errorRatio = checkDuoCarpool.calcErrorRatio(errorRecords.length, duoResults.length);
console.log(`Error ratio: ${(errorRatio * 100).toFixed(2)}%`);
```

### Individual Record Analysis
```javascript
// Analyze specific trip IDs
const tripIds = [12345, 67890];
const trajectories = await checkDuoCarpool.getTrajectoryByTripId(tripIds);

console.log(`Found ${trajectories.length} trajectories for ${tripIds.length} trips`);
trajectories.forEach(traj => {
  console.log(`Trip ${traj.trip_id}: ${traj.points?.length || 0} trajectory points`);
});
```

### Custom Error Detection
```javascript
// Filter for zero-score records with trajectory data
const duoResults = await getDuoResultsByPeriod(['2023-12-01T22:00:00Z', '2023-12-02T22:00:00Z']);
const zeroScoreRecords = duoResults.filter(record => record.score === 0);

console.log(`${zeroScoreRecords.length} records with zero scores out of ${duoResults.length} total`);

// Check which ones have trajectory data (potential errors)
for (const record of zeroScoreRecords) {
  const trajectories = await getTrajectoryByTripId([record.driver_trip_id, record.passenger_trip_id]);
  
  if (trajectories.length === 2) {
    console.log(`ERROR: Record ${record.id} has both trajectories but zero score`);
    console.log(`  Driver trip: ${record.driver_trip_id}`);
    console.log(`  Passenger trip: ${record.passenger_trip_id}`);
    console.log(`  Created: ${record.created_on}`);
  }
}
```

### Metrics Reporting
```javascript
// Report metrics to InfluxDB
const metrics = {
  total_duo_records: 1250,
  zero_score_records: 45,
  error_records: 3,
  error_ratio: 0.0024,
  processing_time_ms: 1500,
};

await checkDuoCarpool.writeResultToInfluxDB(metrics);
console.log('Metrics reported to InfluxDB for monitoring');
```

### Time Period Utilities
```javascript
// Get current analysis period
const [yesterday, today] = checkDuoCarpool.getPeriod();

// Example output:
// yesterday: "2023-11-30T22:00:00.000Z"
// today: "2023-12-01T21:59:59.000Z"

// Custom period generation
const customPeriod = moment().utc().subtract(7, 'days');
const weekAgo = customPeriod.toISOString();
const now = moment().utc().toISOString();

const weeklyResults = await getDuoResultsByPeriod([weekAgo, now]);
```

The checkDuoCarpool service provides essential quality assurance for the carpool validation system, enabling proactive monitoring and identification of scoring anomalies that could impact user experience and system reliability.