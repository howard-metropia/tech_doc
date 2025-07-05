# Check Carpool Records Job

## Overview
Job that validates carpool (duo) validation results and monitors error rates, writing metrics to InfluxDB for monitoring and alerting.

## File Location
`/src/jobs/check-carpool-records.js`

## Dependencies
- `@maas/core/log` - Logging framework
- `@app/src/services/checkDuoCarpool` - Carpool validation service

## Job Configuration

### Inputs
```javascript
inputs: {}
```
No input parameters required.

## Core Functionality

### Validation Process
1. **Period Determination**
   ```javascript
   const period = getPeriod();
   ```
   - Gets appropriate time period for analysis
   - Determines data collection timeframe

2. **Data Retrieval**
   ```javascript
   const duoResultRecords = await getDuoResultsByPeriod(period);
   ```
   - Retrieves carpool validation results for the period
   - Returns early with zero metrics if no records found

3. **Error Detection**
   ```javascript
   const errorRecordList = await getErrorRecords(duoResultRecords);
   ```
   - Analyzes duo results for validation errors
   - Identifies problematic carpool records

### Metrics Calculation
```javascript
const errorRatio = calcErrorRatio(errorDuoRecordCount, totalDuoRecordCount);
const fields = {
  error_count: errorDuoRecordCount,
  duo_validated_result_total: totalDuoRecordCount,
  error_ratio: errorRatio
};
```

### No Data Scenario
```javascript
if (!duoResultRecords || duoResultRecords.length === 0) {
  const fields = {
    error_count: 0,
    duo_validated_result_total: 0,
    error_ratio: 0
  };
  await writeResultToInfluxDB(fields);
  return;
}
```

## Error Handling and Logging

### Error Record Logging
```javascript
if (errorRecordList.length > 0) {
  const msg = {
    content: 'error carpool records found',
    data: errorRecordList
  };
  logger.error(msg);
}
```

### Success Logging
```javascript
logger.info(
  `writing to duo_score_error, error_count: ${errorDuoRecordCount}, total_count: ${totalDuoRecordCount}`
);
```

## InfluxDB Integration

### Metrics Storage
```javascript
await writeResultToInfluxDB(fields);
```

### Metric Fields
- **error_count**: Number of problematic carpool records
- **duo_validated_result_total**: Total carpool validation attempts  
- **error_ratio**: Percentage of failed validations

## Service Dependencies

### checkDuoCarpool Service Functions
- **getPeriod()**: Determines analysis timeframe
- **getDuoResultsByPeriod()**: Retrieves validation results
- **getErrorRecords()**: Identifies error records
- **writeResultToInfluxDB()**: Stores metrics in time-series database
- **calcErrorRatio()**: Calculates error percentage

## Data Quality Monitoring

### Validation Metrics
- Tracks carpool validation success/failure rates
- Monitors system reliability over time
- Enables alerting on high error rates

### Error Analysis
- Logs detailed error records for investigation
- Provides data for improving validation algorithms
- Supports troubleshooting of carpool matching issues

## Performance Considerations
- Processes data in configurable time periods
- Writes zero metrics when no data available
- Efficient error ratio calculations
- Minimal database impact with batch processing

## Usage Context
- **Carpool Validation**: Monitors duo carpool matching accuracy
- **System Health**: Tracks validation system performance
- **Data Quality**: Ensures carpool data integrity
- **Alerting**: Enables monitoring dashboards and alerts

## Related Components
- Carpool validation system
- InfluxDB time-series database
- Monitoring and alerting infrastructure
- Carpool matching algorithms

## Schedule Context
Typically scheduled to run at regular intervals to continuously monitor carpool validation quality and system performance.