# HNTB ETL Job

## Overview
Extract, Transform, Load (ETL) job that orchestrates data processing for HNTB (Houston-Galveston Area Council transportation consultant) analytics and reporting. This job coordinates multiple ETL services to process transportation data, user analytics, and geographic information for comprehensive transportation analysis and reporting.

## File Location
`/src/jobs/hntb-etl.js`

## Dependencies
- `@maas/core/log` - Logging framework for operational monitoring
- `@app/src/services/hntb-etl` - HNTB ETL service collection containing all data processing functions

## Job Configuration

### Inputs
```javascript
inputs: {
  start: String,  // Start date for data processing range
  end: String     // End date for data processing range
}
```

### Date Handling Logic
```javascript
if (start === '') start = 'null';
if (end === '') end = 'null';
```
Empty strings are converted to 'null' to trigger automatic date range detection in ETL services.

## ETL Processing Workflow

### Phase 1: Data Preparation
**County Data Backfill**:
```javascript
await etl.fillCounty();
```
- Fills missing county information in historical data
- Ensures geographic completeness for analysis
- Updates location records with proper county assignments

**Target User List Update**:
```javascript
await etl.checkTargetUser();
```
- Updates and validates target user list for analysis
- Ensures user eligibility and data quality
- Maintains current user status for reporting

### Phase 2: User Exclusion Processing
**Exclude User ID Retrieval**:
```javascript
const excludeUserIds = await etl.fetchExcludeUserIds();
```
- Retrieves list of users to exclude from processing
- Handles test accounts, invalid users, and opt-out users
- Provides clean dataset for analysis

### Phase 3: Dynamic Service Execution

**Service Discovery**:
```javascript
const services = Object.keys(etl);
```

**Service Filtering**:
```javascript
if (service === 'fetchExcludeUserIds' || 
    service === 'checkTargetUser' || 
    service === 'checkCounty' || 
    service === 'fillCounty') continue;
```

**Dynamic Service Execution**:
```javascript
for (const service of services) {
  try {
    await etl[service](start, end, excludeUserIds);
  } catch (err) {
    logger.error(`${service} failed:${err.message}`);
    failed = true;
  }
}
```

## ETL Service Integration

### Service Parameters
All ETL services receive standardized parameters:
- `start`: Start date for data processing
- `end`: End date for data processing  
- `excludeUserIds`: Array of user IDs to exclude from processing

### Service Types
The HNTB ETL service collection typically includes:
- **Trip Data Processing**: Journey analysis and aggregation
- **User Behavior Analytics**: Usage patterns and preferences
- **Geographic Analysis**: Location-based insights
- **Performance Metrics**: System and user performance data
- **Reporting Data**: Formatted data for business intelligence

## Error Handling Strategy

### Individual Service Error Tracking
```javascript
let failed = false;
try {
  await etl[service](start, end, excludeUserIds);
} catch (err) {
  logger.error(`${service} failed:${err.message}`);
  failed = true;
}
```

### Comprehensive Error Reporting
```javascript
if (failed) {
  throw new Error(`hntb-etl job failed, check the logs!`);
}
```

**Error Handling Approach**:
- Continue processing other services even if one fails
- Log each service failure with specific error messages
- Throw aggregate error if any service fails
- Enables partial data processing and detailed error tracking

## Data Quality Assurance

### Pre-Processing Validation
1. **County Data Integrity**: Ensures all records have proper geographic assignment
2. **Target User Validation**: Confirms user eligibility and data completeness
3. **Exclusion List Updates**: Maintains current list of users to exclude

### Processing Isolation
- Each ETL service operates independently
- Service failures don't cascade to other processes
- Allows for granular error diagnosis and recovery

## Service Architecture

### Modular Design
```javascript
const services = Object.keys(etl);
```
- Dynamically discovers available ETL services
- Enables easy addition of new processing services
- Maintains consistent parameter interface across services

### Service Exclusion Logic
Protected services (utility functions) are excluded from dynamic execution:
- `fetchExcludeUserIds`: User exclusion data retrieval
- `checkTargetUser`: User validation service
- `checkCounty`: Geographic validation service
- `fillCounty`: County data backfill service

## Performance Considerations

### Sequential Processing
Services are executed sequentially to:
- Maintain data consistency across processing steps
- Avoid database connection pool exhaustion
- Enable proper error tracking and recovery

### Memory Management
- Each service processes data independently
- No shared state between services
- Efficient resource utilization through service isolation

## Integration Points

### HNTB ETL Service Collection
The job orchestrates multiple specialized services:
- **Data Extraction**: From various transportation data sources
- **Data Transformation**: Cleaning, validation, and formatting
- **Data Loading**: Into analytics and reporting systems
- **Quality Assurance**: Data validation and integrity checks

### External Dependencies
- Database systems for source and destination data
- Geographic information services for location processing
- User management systems for validation and exclusion

## Monitoring and Logging

### Service-Level Logging
```javascript
logger.error(`${service} failed:${err.message}`);
```
- Individual service success/failure tracking
- Detailed error message capture
- Service-specific performance monitoring

### Job-Level Status
- Overall job success/failure determination
- Comprehensive error aggregation for alerting
- Processing statistics and performance metrics

## Schedule Context
Typically scheduled to run on a regular basis (daily or weekly) to:
- Process transportation data for HNTB analysis
- Generate reports for transportation planning
- Update analytics databases with current data
- Maintain data quality and completeness

## Business Impact
- Provides critical transportation data for Houston-Galveston Area Council
- Supports transportation planning and policy decisions
- Enables performance monitoring of transportation systems
- Delivers analytics for public transportation optimization
- Maintains data pipeline integrity for stakeholder reporting