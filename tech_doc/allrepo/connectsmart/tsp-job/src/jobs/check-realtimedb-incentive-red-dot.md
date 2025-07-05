# Check Realtime Database Incentive Red Dot Job

## Overview
Scheduled job that monitors and updates the red dot status for incentive notifications in the real-time database. This job ensures that users see appropriate visual indicators for new or updated incentive offers that require their attention.

## File Location
`/src/jobs/check-realtimedb-incentive-red-dot.js`

## Dependencies
- `@maas/core/log` - Centralized logging framework for job execution tracking
- `config` - Configuration management for project settings
- `@app/src/services/realtimedb` - Real-time database service layer for Firebase/Redis operations

## Job Configuration

### Inputs
```javascript
inputs: {}  // No input parameters required
```

### Module Structure
```javascript
module.exports = {
  inputs: {},
  fn: async function () {
    // Job execution logic
  }
}
```

## Core Functionality

### Main Execution Flow
```javascript
fn: async function () {
  logger.info('[check-realtimedb-incentive-red-dot] start');
  try {
    checkRedDotStatus()
  } catch (e) {
    logger.error(`[check-realtimedb-incentive-red-dot] error: ${e.message}`);
    logger.info(`[check-realtimedb-incentive-red-dot] stack: ${e.stack}`);
  }
}
```

**Process Steps**:
1. **Initialization**: Logs job start with standardized identifier
2. **Red Dot Check**: Calls `checkRedDotStatus()` from realtime database service
3. **Error Handling**: Comprehensive error logging with message and stack trace

## Service Integration

### Real-time Database Service
The job delegates core functionality to the `checkRedDotStatus()` function from the realtime database service:

```javascript
const { checkRedDotStatus } = require('@app/src/services/realtimedb');
```

**Service Responsibilities**:
- Query user incentive status from database
- Determine which users need red dot indicators
- Update real-time database with current status
- Handle user notification state management

## Red Dot Status Logic

### Typical Red Dot Scenarios
1. **New Incentives**: Users with unviewed incentive offers
2. **Updated Offers**: Previously seen incentives with changed terms
3. **Expiring Soon**: Time-sensitive incentives requiring user action
4. **Achievement Unlocked**: New rewards or badges earned

### Status Update Process
- **Database Query**: Retrieve user incentive interaction history
- **Status Calculation**: Determine if red dot should be shown
- **Real-time Update**: Push status changes to connected clients
- **Cache Management**: Update cached notification states

## Error Handling

### Exception Management
```javascript
catch (e) {
  logger.error(`[check-realtimedb-incentive-red-dot] error: ${e.message}`);
  logger.info(`[check-realtimedb-incentive-red-dot] stack: ${e.stack}`);
}
```

**Error Scenarios**:
- Database connection failures
- Real-time database synchronization issues
- Service unavailability
- Data integrity problems

### Logging Strategy
- **Start Logging**: Job initiation tracking
- **Error Logging**: Both error messages and stack traces
- **Consistent Naming**: Standardized job identifier for log filtering

## Configuration Dependencies

### Project Configuration
```javascript
const config = require('config').project;
```

**Configuration Elements**:
- Real-time database connection settings
- Incentive system parameters
- Notification timing configurations
- Feature flags for red dot behavior

## Performance Considerations

### Lightweight Design
- **Minimal Processing**: Delegates heavy lifting to service layer
- **Fast Execution**: Simple wrapper around service function
- **Error Resilience**: Continues operation despite individual failures

### Resource Management
- **Memory Efficient**: No data caching in job itself
- **Connection Pooling**: Relies on service layer for database connections
- **Async Operations**: Non-blocking execution pattern

## Integration Points

### Real-time Database Service
- Primary integration point for all red dot logic
- Handles database operations and state management
- Provides abstraction layer for complex notification logic

### Logging Infrastructure
- Integrates with centralized logging system
- Enables monitoring and debugging capabilities
- Supports operational troubleshooting

## Scheduling Context
This job is typically scheduled to run at regular intervals (e.g., every 5-15 minutes) to ensure users receive timely visual feedback about their incentive status. The frequency depends on user engagement patterns and real-time notification requirements.

## Related Components
- Incentive management system
- User notification framework
- Real-time database synchronization
- Mobile application UI components
- Push notification services

## Operational Monitoring
The job provides clear logging for operational monitoring:
- **Execution Tracking**: Start/completion logging
- **Error Visibility**: Detailed error information
- **Performance Metrics**: Through centralized logging analysis