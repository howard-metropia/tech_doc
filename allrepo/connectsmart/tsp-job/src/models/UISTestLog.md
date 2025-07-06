# UISTestLog Model

## Overview
MongoDB model for logging User Interface System (UIS) test operations and incident management processes. This model provides structured logging capabilities for tracking system tests, incident event processing, and operational monitoring within the TSP system's incident management infrastructure.

## File Location
`/src/models/UISTestLog.js`

## Model Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const recordSchema = new Schema(
  {
    time: {
      type: String,
      required: true,
    },
    log: {
      type: String,
      required: true,
    },
  },
  { _id: false },
);

const schema = new Schema({
  record_id: {
    type: String,
    index: true,
    required: true,
  },
  records: {
    type: [recordSchema],
    required: true,
  },
});
schema.index({ record_id: 1 });
const UISTestLog = conn.model('uis_test_log', schema);

module.exports = UISTestLog;
```

## Database Configuration
- **Database**: MongoDB cache instance
- **Collection**: `uis_test_log`
- **Framework**: Mongoose ODM
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Schema Mode**: Strict schema with defined structure and validation

## Schema Structure

### Main Document Schema
#### record_id
- **Type**: String
- **Required**: Yes
- **Indexed**: Yes (with explicit index definition)
- **Purpose**: Unique identifier for the test session or incident event
- **Format**: Typically combines event ID and timestamp (e.g., "eventId123T2023-10-15")

#### records
- **Type**: Array of recordSchema documents
- **Required**: Yes
- **Purpose**: Collection of chronological log entries for the test session
- **Structure**: Each record contains time and log information

### Record Sub-Schema
#### time
- **Type**: String
- **Required**: Yes
- **Purpose**: Timestamp when the log entry was created
- **Format**: "YYYY-MM-DD HH:mm:ss" UTC format
- **Example**: "2023-10-15 14:30:25"

#### log
- **Type**: String
- **Required**: Yes
- **Purpose**: Detailed log message describing the test operation or event
- **Content**: Test results, error messages, status updates, incident details

## Purpose and Functionality
- **Test Session Logging**: Track comprehensive test operations and results
- **Incident Event Processing**: Log incident management operations and status changes
- **Operational Monitoring**: Provide audit trail for system test procedures
- **Debugging Support**: Detailed logging for troubleshooting test failures

## Key Features
- **Hierarchical Structure**: Groups related log entries under common record IDs
- **Chronological Ordering**: Time-stamped log entries for sequence analysis
- **Indexed Access**: Optimized queries by record_id for fast retrieval
- **Structured Logging**: Consistent format for log analysis and processing

## Integration with Incident Management
The model is primarily used by the **update-incident-events.js** job for logging test operations:

```javascript
// From update-incident-events.js
const UISTestLog = require('@app/src/models/UISTestLog');

const recordTestLog = async (eventId, time, log) => {
  try {
    const nowTime = moment.utc().format('YYYY-MM-DD HH:mm:ss');
    await UISTestLog.updateOne(
      {
        record_id: `${eventId}T${time}`,
      }, // filter
      {
        $push: { records: { time: nowTime, log: log } },
      }, // update
      { upsert: true } // options
    );
  } catch (error) {
    logger.error('Error recording test log:', error);
  }
};
```

## Usage Patterns

### Creating New Test Session
```javascript
// Initialize new test log session
const testSession = {
  record_id: 'incident_123T2023-10-15',
  records: [{
    time: '2023-10-15 14:30:00',
    log: 'Test session initiated for incident event 123'
  }]
};

await UISTestLog.create(testSession);
```

### Appending Log Entries
```javascript
// Add new log entry to existing session
await UISTestLog.updateOne(
  { record_id: 'incident_123T2023-10-15' },
  {
    $push: {
      records: {
        time: '2023-10-15 14:31:15',
        log: 'Route calculation completed successfully'
      }
    }
  }
);
```

### Retrieving Test Logs
```javascript
// Get complete test session
const testSession = await UISTestLog.findOne({
  record_id: 'incident_123T2023-10-15'
});

// Get recent test sessions
const recentTests = await UISTestLog.find({
  record_id: { $regex: /^incident_.*T2023-10/ }
}).sort({ 'records.time': -1 });
```

## Incident Event Integration
The model supports various incident management operations:

### Route Planning Tests
- **HERE API Integration**: Test route calculations using HERE Maps
- **Algorithm Validation**: Verify routing algorithm performance
- **Response Time Monitoring**: Track API response times
- **Error Handling**: Log routing failures and recovery attempts

### Notification System Tests
- **Alert Generation**: Test incident alert creation
- **Notification Delivery**: Verify notification system functionality
- **User Targeting**: Test notification targeting algorithms
- **Delivery Confirmation**: Track notification delivery status

### Calendar Event Processing
- **Event Synchronization**: Test calendar event integration
- **Scheduling Validation**: Verify event scheduling accuracy
- **Conflict Resolution**: Test scheduling conflict handling
- **Update Processing**: Log event update operations

## Operational Workflows

### Incident Test Lifecycle
1. **Test Initiation**: Create new test session with initial log entry
2. **Process Execution**: Log each step of the incident processing
3. **Result Validation**: Record test results and validation outcomes
4. **Error Handling**: Log any errors or exceptions encountered
5. **Session Completion**: Final log entry marking test completion

### Continuous Monitoring
1. **Scheduled Tests**: Regular system health checks
2. **Performance Monitoring**: Track system performance metrics
3. **Alert Generation**: Create alerts for test failures
4. **Trend Analysis**: Analyze test patterns over time

## Query Patterns for Analysis

### Test Session Analysis
```javascript
// Get all records for a specific event
const eventLogs = await UISTestLog.find({
  record_id: { $regex: /^incident_123T/ }
});

// Find failed tests
const failedTests = await UISTestLog.find({
  'records.log': { $regex: /error|failed|exception/i }
});
```

### Performance Analysis
```javascript
// Analyze test duration patterns
const testDurations = await UISTestLog.aggregate([
  { $unwind: '$records' },
  {
    $group: {
      _id: '$record_id',
      start_time: { $min: '$records.time' },
      end_time: { $max: '$records.time' },
      log_count: { $sum: 1 }
    }
  }
]);
```

## Performance Considerations
- **Index Optimization**: record_id field is indexed for fast queries
- **Document Size**: Monitor document growth as records array expands
- **Query Efficiency**: Use record_id patterns for targeted queries  
- **Memory Usage**: Consider memory implications of large record arrays

## Monitoring and Analytics Applications
- **Test Success Rates**: Track percentage of successful tests
- **Performance Trends**: Monitor test execution time trends
- **Error Pattern Analysis**: Identify common failure patterns
- **System Health**: Overall system reliability metrics

## Integration Points
- **update-incident-events.js**: Primary integration for incident processing
- **CalendarEvents Model**: Calendar integration testing
- **NotificationRecord Model**: Notification system testing
- **IncidentsEvent Model**: Incident management operations
- **HERE API Service**: Route planning test integration

## Data Retention and Management
- **Log Rotation**: Consider rotating old test logs to prevent unlimited growth
- **Archive Strategy**: Move historical test data to archival storage
- **Cleanup Procedures**: Regular maintenance of test log collections
- **Storage Optimization**: Balance detail level with storage requirements

## Error Handling and Recovery
- **Exception Logging**: Comprehensive error capture and logging
- **Retry Logic**: Log retry attempts and outcomes
- **Fallback Procedures**: Document fallback operation logs
- **Recovery Tracking**: Monitor system recovery after failures

## Security and Access Control
- **Log Sanitization**: Ensure no sensitive data in logs
- **Access Restrictions**: Control access to test logs
- **Audit Compliance**: Maintain logs for audit requirements
- **Data Privacy**: Protect any user-related information in logs

## Development and Testing
- **Test Environment**: Separate test logging from production
- **Debug Support**: Rich logging for development troubleshooting
- **Performance Testing**: Monitor logging performance impact
- **Schema Validation**: Ensure data integrity through schema enforcement

## Future Enhancements
- **Real-time Monitoring**: Add real-time test monitoring capabilities
- **Automated Analysis**: Implement automated log analysis and alerting
- **Dashboard Integration**: Connect logs to monitoring dashboards
- **Machine Learning**: Apply ML for predictive failure analysis

## Troubleshooting Guide
- **Missing Logs**: Check record_id format and indexing
- **Performance Issues**: Review query patterns and indexing strategy
- **Storage Growth**: Monitor document size and implement retention policies
- **Integration Problems**: Verify connection configuration and error handling