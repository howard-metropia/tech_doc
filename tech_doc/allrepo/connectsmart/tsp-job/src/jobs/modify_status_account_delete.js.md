# modify_status_account_delete.js

## Overview
Job module responsible for managing the lifecycle of account deletion verification codes and requests. This job handles the automatic cleanup of expired verification codes, sets expired status for verification codes that have exceeded their validity period, and permanently removes old account deletion records to maintain database hygiene and comply with data retention policies.

## Purpose
- Manage account deletion verification code lifecycle
- Automatically expire verification codes that exceed time limits
- Remove old account deletion records for data retention compliance
- Maintain database cleanliness and performance
- Support account deletion workflow automation

## Key Features
- **Automated Expiration**: Sets expired status for verification codes past their validity period
- **Data Retention Management**: Removes records older than 90 days
- **Status Management**: Updates verification code status from 'created' to 'expired'
- **Efficient Processing**: Single-job execution handles all lifecycle management
- **No Input Parameters**: Fully automated execution based on current time

## Dependencies
```javascript
const moment = require('moment-timezone');
const { logger } = require('@maas/core/log');
const AccountDelete = require('@app/src/models/AccountDelete');
```

## Core Function Structure
```javascript
module.exports = {
  inputs: {},
  fn: async function () {
    // Process expired verification codes
    // Remove old account deletion records
    // Update status for expired requests
  }
};
```

## Processing Logic

### Main Execution Flow
1. **Old Record Cleanup**: Remove account deletion records older than 90 days
2. **Expiration Processing**: Update status of expired verification codes
3. **Logging**: Record processing results and statistics

### Data Retention Management
```javascript
const deleteDataDaysBefore = 90;
const adDatasOfNeedDelete = await AccountDelete.find({
  created_on: {
    $lt: moment().utc().subtract(deleteDataDaysBefore, 'days').endOf('day')
  }
});

if (adDatasOfNeedDelete.length > 0) {
  await AccountDelete.deleteMany({
    created_on: {
      $lt: moment().utc().subtract(deleteDataDaysBefore, 'days').endOf('day')
    }
  });
}
```

## Account Deletion Lifecycle

### Verification Code States
- **created**: Initial state when verification code is generated
- **expired**: Code has exceeded its validity period
- **completed**: Account deletion has been processed (handled elsewhere)

### Status Transition Process
```javascript
const adDeleteDatasWithExpired = await AccountDelete.find({
  status: 'created',
  expire_on: {
    $lt: moment()
  }
});

if (adDeleteDatasWithExpired.length > 0) {
  await Promise.all(
    adDeleteDatasWithExpired.map(async (item) => {
      await AccountDelete.updateOne(
        { uuid: item.uuid },
        {
          $set: {
            status: 'expired',
            updated_on: moment.utc().toISOString()
          }
        },
        { upsert: true }
      );
    })
  );
}
```

## Data Model Integration

### AccountDelete Model Fields
- **uuid**: Unique identifier for account deletion request
- **status**: Current state of verification process
- **created_on**: Timestamp when request was created
- **expire_on**: Timestamp when verification code expires
- **updated_on**: Last modification timestamp

### Database Operations
- **Find Operations**: Query for records based on time criteria
- **Update Operations**: Modify status and timestamps
- **Delete Operations**: Permanent removal of old records

## Time-Based Processing

### 90-Day Retention Policy
```javascript
const deleteDataDaysBefore = 90;
const cutoffDate = moment().utc().subtract(deleteDataDaysBefore, 'days').endOf('day');
```

### Expiration Check Logic
```javascript
const currentTime = moment();
const expiredRecords = await AccountDelete.find({
  status: 'created',
  expire_on: { $lt: currentTime }
});
```

## Database Operations

### Bulk Deletion
- Removes all records older than retention period
- Uses MongoDB deleteMany for efficient batch removal
- Processes based on created_on timestamp

### Individual Updates
- Updates each expired verification code individually
- Sets status to 'expired' with current timestamp
- Maintains audit trail with updated_on field

## Error Handling Strategy

### Implicit Error Handling
- MongoDB operations include built-in error handling
- Database connection errors handled at service level
- Individual update failures don't affect other records

### Transaction Safety
- Uses MongoDB atomic operations for data consistency
- Individual record updates prevent partial failures
- Proper timestamping for audit purposes

## Logging and Monitoring

### Cleanup Logging
```javascript
logger.info(
  `delete ${adDatasOfNeedDelete.length} row${
    adDatasOfNeedDelete.length > 1 ? 's' : ''
  } delete account log success`
);
```

### Expiration Logging
```javascript
logger.info(
  `modify status ${adDeleteDatasWithExpired.length} row${
    adDeleteDatasWithExpired.length > 1 ? 's' : ''
  } success`
);
```

### Process Tracking
```javascript
logger.info('set expired status or delete of delete account verification code start');
logger.info('set expired status or delete of delete account verification code end');
```

## Performance Considerations

### Efficient Queries
- Time-based filtering reduces processing load
- Indexed queries on created_on and expire_on fields
- Bulk operations minimize database round trips

### Resource Management
- Single-pass processing for each operation type
- Minimal memory footprint with streaming operations
- Efficient MongoDB query patterns

## Security Considerations

### Data Privacy Compliance
- Automatic removal of old personal data requests
- Maintains audit trail for compliance purposes
- Secure handling of user deletion requests

### Access Control
- Database-level access controls for AccountDelete collection
- Audit logging for data retention compliance
- Proper authentication for database operations

## Integration Points

### Account Management System
- Supports account deletion workflow
- Integrates with user verification processes
- Maintains consistency with user management operations

### Compliance Systems
- Supports data retention policy enforcement
- Provides audit trails for regulatory compliance
- Handles privacy regulation requirements

## Use Cases

### Automated Maintenance
- Regular cleanup of expired verification codes
- Maintenance of database performance and storage
- Automated compliance with data retention policies

### Verification Code Management
- Prevents indefinite pending verification states
- Maintains accurate status of deletion requests
- Supports user experience with timely status updates

## Operational Workflow

### Scheduled Execution
- Typically executed daily or weekly
- Can be run multiple times safely (idempotent)
- No dependencies on external services

### Manual Execution
- Safe for on-demand execution
- Useful for maintenance and cleanup operations
- No side effects on other system components

## Configuration Management

### Time Period Configuration
```javascript
const deleteDataDaysBefore = 90; // Configurable retention period
```

### Timezone Handling
- Uses UTC timestamps for consistency
- Proper timezone conversion with moment.js
- Handles daylight saving time transitions

## Deployment Considerations

### Database Requirements
- MongoDB with AccountDelete collection
- Proper indexes on created_on and expire_on fields
- Sufficient permissions for delete and update operations

### Scheduling Requirements
- Regular execution schedule (daily/weekly recommended)
- No external service dependencies
- Minimal resource requirements

## Data Retention Compliance

### Regulatory Support
- Supports GDPR and similar privacy regulations
- Automated data removal for compliance
- Audit trail maintenance for verification

### Policy Enforcement
- Configurable retention periods
- Automated enforcement of data policies
- Consistent application across all records

## Future Enhancements
- Configurable retention periods via configuration files
- Enhanced logging with detailed statistics
- Support for different retention policies by request type
- Integration with compliance reporting systems
- Advanced error handling and retry mechanisms
- Performance monitoring and optimization features