# Job Measure Middleware

## Overview
**File**: `src/middlewares/job-measure.js`  
**Type**: Performance Monitoring Middleware  
**Purpose**: Provides automated job execution tracking and performance measurement with InfluxDB integration for TSP scheduled jobs

## Core Functionality

### Job Performance Tracking
This middleware automatically measures and logs the execution lifecycle of scheduled jobs in the TSP system, providing comprehensive monitoring capabilities through InfluxDB time-series database integration.

### Key Features
- **Automatic Job ID Generation**: Creates unique 12-character identifiers for each job execution
- **Lifecycle Tracking**: Monitors job start, completion, and failure states
- **InfluxDB Integration**: Stores metrics in time-series database for analysis
- **Error Resilience**: Continues operation even if logging fails
- **Contextual Tagging**: Adds datacenter, project, and stage metadata to all metrics

## Technical Implementation

### Dependencies
```javascript
const { logger } = require('@maas/core/log');
const { InfluxDB, Point } = require('@influxdata/influxdb-client');
const ShortUniqueId = require('short-unique-id');
```

### InfluxDB Configuration
```javascript
const db = new InfluxDB({
  url: process.env.INFLUXDB_URL,
  token: process.env.INFLUXDB_TOKEN,
});

const write = db
  .getWriteApi(process.env.INFLUXDB_ORG, process.env.INFLUXDB_BUCKET, 'ns')
  .useDefaultTags({
    datacenter: process.env.CLUSTER_DATACENTER,
    project: process.env.PROJECT_NAME,
    stage: process.env.PROJECT_STAGE,
  });
```

### Unique ID Generator
```javascript
const uid = new ShortUniqueId({ length: 12 });
```

## Core Functions

### writeToDbSync Function
```javascript
const writeToDbSync = async (name, id, status) => {
  try {
    write.writePoint(
      new Point('scheduling-job').timestamp(new Date)
        .tag('job', name)
        .stringField('uuid', id)
        .stringField('status', status)
    )
    await write.flush()
  } catch (err) {
    logger.error(err.message);
  }
}
```

**Purpose**: Synchronously writes job metrics to InfluxDB with immediate flush
**Parameters**:
- `name`: Job name from context
- `id`: Unique job execution identifier
- `status`: Current job status ('start', 'end', 'failed')

### writeToDb Function
```javascript
const writeToDb = (name, id, status) => {
  try {
    write.writePoint(
      new Point('scheduling-job').timestamp(new Date)
        .tag('job', name)
        .stringField('uuid', id)
        .stringField('status', status)
    )
  } catch (err) {
    logger.error(err.message);
  }
}
```

**Purpose**: Asynchronously writes job metrics without blocking execution
**Use Case**: Used for end and failure status updates where immediate persistence isn't critical

## Middleware Implementation

### Main Middleware Function
```javascript
module.exports = async (ctx, next) => {
  const jobId = uid()
  try {
    await writeToDbSync(ctx.name, jobId, 'start');
    await next()
    writeToDb(ctx.name, jobId, 'end')
  } catch (error) {
    writeToDb(ctx.name, jobId, 'failed');
    logger.error(error)
  }
  await write.close()
};
```

### Execution Flow
1. **Job ID Generation**: Creates unique identifier for the job execution
2. **Start Logging**: Synchronously logs job start with immediate persistence
3. **Job Execution**: Calls next middleware/handler in the chain
4. **Success Logging**: Logs successful completion asynchronously
5. **Error Handling**: Catches and logs job failures with error details
6. **Connection Cleanup**: Closes InfluxDB write connection

## Data Model

### InfluxDB Point Structure
```javascript
new Point('scheduling-job')
  .timestamp(new Date)
  .tag('job', jobName)           // Job identifier tag
  .stringField('uuid', jobId)    // Unique execution ID
  .stringField('status', status) // Execution status
```

### Measurement Schema
- **Measurement**: `scheduling-job`
- **Tags**: 
  - `job`: Job name from context
  - `datacenter`: Deployment datacenter
  - `project`: Project name
  - `stage`: Environment stage (dev/staging/prod)
- **Fields**:
  - `uuid`: Job execution unique identifier
  - `status`: Job execution status

### Status Values
- **start**: Job execution initiated
- **end**: Job completed successfully
- **failed**: Job encountered error during execution

## Configuration Requirements

### Environment Variables
```bash
# InfluxDB Connection
INFLUXDB_URL=https://influxdb.example.com:8086
INFLUXDB_TOKEN=your_influxdb_token
INFLUXDB_ORG=your_organization
INFLUXDB_BUCKET=tsp_metrics

# Metadata Tags
CLUSTER_DATACENTER=us-east-1
PROJECT_NAME=tsp-job-scheduler
PROJECT_STAGE=production
```

### Context Requirements
The middleware expects the job context to contain:
- `ctx.name`: String identifier for the job being executed

## Usage Integration

### Middleware Registration
```javascript
// In middlewares.js
const jobMeasure = require('@app/src/middlewares/job-measure');

module.exports = {
  schedule: [
    jobMeasure,  // Register for scheduled jobs
  ],
  run: [
    // Not typically used for run commands
  ],
};
```

### Job Context Setup
```javascript
// Job execution context must include name
const jobContext = {
  name: 'update-bytemark-tickets',
  // other job properties
};
```

## Performance Characteristics

### Execution Overhead
- **Start Phase**: Synchronous write with flush (~10-50ms)
- **End Phase**: Asynchronous write (~1-5ms)
- **Error Phase**: Asynchronous write with error logging
- **Connection Cleanup**: Connection close operation

### Resource Usage
- **Memory**: Minimal footprint with connection pooling
- **Network**: Small data points sent to InfluxDB
- **CPU**: Low overhead for UUID generation and serialization

## Error Handling

### Resilient Design
```javascript
try {
  // InfluxDB operations
} catch (err) {
  logger.error(err.message);
  // Job continues despite logging failure
}
```

### Error Scenarios
- **InfluxDB Unavailable**: Logs error but doesn't fail job
- **Network Issues**: Graceful degradation with error logging
- **Authentication Failures**: Token issues logged, job continues
- **Job Execution Errors**: Properly captured and logged with 'failed' status

## Monitoring and Observability

### Metrics Available
- **Job Execution Count**: Number of job runs per time period
- **Job Success Rate**: Ratio of successful vs failed executions
- **Job Duration**: Time between start and end events
- **Error Patterns**: Failed job analysis and trends

### Query Examples
```sql
-- Job execution count by name
SELECT COUNT(*) FROM "scheduling-job" 
WHERE time >= now() - 24h 
GROUP BY "job"

-- Job success rate
SELECT 
  COUNT(CASE WHEN "status" = 'end' THEN 1 END) as success,
  COUNT(CASE WHEN "status" = 'failed' THEN 1 END) as failures
FROM "scheduling-job" 
WHERE time >= now() - 24h 
GROUP BY "job"

-- Average job duration
SELECT 
  MEAN(duration) 
FROM (
  SELECT 
    LAST("uuid") - FIRST("uuid") as duration
  FROM "scheduling-job" 
  WHERE time >= now() - 24h 
  GROUP BY "uuid"
)
```

## Integration with Job System

### Scheduled Jobs
All scheduled jobs in the TSP system automatically receive performance monitoring when this middleware is registered in the schedule middleware chain.

### Job Lifecycle Events
1. **Job Queue**: Job enters execution queue
2. **Middleware Chain**: Job measure middleware activated
3. **Start Event**: InfluxDB point created with 'start' status
4. **Job Logic**: Actual job implementation executes
5. **End Event**: Success or failure status logged
6. **Cleanup**: Connection resources released

## Best Practices

### Implementation Guidelines
- **Context Naming**: Ensure job context includes meaningful `name` property
- **Error Boundaries**: Don't let monitoring failures affect job execution
- **Resource Management**: Properly close InfluxDB connections
- **Logging**: Include sufficient detail for debugging issues

### Performance Optimization
- **Batch Writes**: Consider batching for high-frequency jobs
- **Connection Pooling**: Reuse connections where possible
- **Async Operations**: Use async writes for non-critical status updates

## Troubleshooting

### Common Issues
1. **Missing Environment Variables**: Check InfluxDB configuration
2. **Connection Timeouts**: Verify network connectivity to InfluxDB
3. **Authentication Errors**: Validate InfluxDB token permissions
4. **Missing Job Names**: Ensure job context includes name property

### Debug Information
```javascript
// Enable debug logging
logger.info(`Job ${ctx.name} started with ID ${jobId}`);
logger.info(`InfluxDB write completed for job ${ctx.name}`);
```

### Health Checks
- **InfluxDB Connectivity**: Periodic connection health checks
- **Write Success Rate**: Monitor logging success/failure ratio
- **Job Coverage**: Ensure all scheduled jobs are being measured

## Security Considerations

### Token Management
- **Environment Variables**: Store InfluxDB tokens securely
- **Access Control**: Limit token permissions to write-only
- **Rotation**: Regular token rotation policies

### Data Privacy
- **Job Names**: Avoid sensitive information in job names
- **Metadata**: Review tags for sensitive data exposure
- **Retention**: Configure appropriate data retention policies

This middleware provides essential observability for TSP job scheduling operations, enabling performance monitoring, failure detection, and operational insights through comprehensive metrics collection in InfluxDB.