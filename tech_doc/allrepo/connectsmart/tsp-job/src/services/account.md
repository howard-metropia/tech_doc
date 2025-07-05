# Account Service

## Overview

The Account service manages user account cleanup operations, specifically handling the deletion of backup account data based on user deletion events with configurable retention periods.

## Service Information

- **Service Name**: Account
- **File Path**: `/src/services/account.js`
- **Type**: Account Management Service
- **Dependencies**: MySQL, MongoDB, Account Models

## Functions

### deleteBackupAccount()

Removes backup account data for users who have requested account deletion.

**Purpose**: Cleans up backup account data after configurable retention period
**Parameters**: None (processes deletion events from database)
**Returns**: Promise (async function)

**Process Flow**:
1. Verifies required database tables exist
2. Identifies deletion events older than retention period
3. Removes backup user data from multiple storage systems
4. Updates deletion event status to prevent reprocessing
5. Logs cleanup results for monitoring

**Retention Period**: 90 days from deletion event creation

**Example**:
```javascript
await deleteBackupAccount();
// Processes deletion events older than 90 days
// Logs: "[delete-backup-account] deleted backup account(s) for user(s) 123, 456."
```

## Data Sources

### Required Tables
- **auth_user_bk**: Backup user authentication data
- **auth_user_event**: User lifecycle events including deletions
- **AccountDelete**: MongoDB collection for deletion records

### Event Processing
- **Event Type**: 'delete' events in auth_user_event table
- **Time Filter**: Events older than 90-day retention period
- **Status Tracking**: purge_status field prevents duplicate processing

## Deletion Process

### Multi-Storage Cleanup
1. **MySQL Cleanup**: Removes records from auth_user_bk table
2. **MongoDB Cleanup**: Removes AccountDelete documents
3. **Status Update**: Marks auth_user_event as purged

### Data Extraction
- **User IDs**: Extracted from deletion events
- **Event IDs**: Tracked for status updates
- **Batch Processing**: Handles multiple users in single operation

### Safety Measures
- **Table Existence Check**: Ensures required tables are available
- **Time Validation**: Only processes events beyond retention period
- **Transaction Safety**: Atomic operations prevent partial deletions

## Error Handling

### Table Validation
- Checks for auth_user_bk and auth_user_event table existence
- Graceful handling when tables are not available
- Informative logging for missing dependencies

### Exception Management
- Comprehensive error logging with stack traces
- Continues operation despite individual deletion failures
- Preserves system stability during cleanup operations

### Logging Strategy
- **Success**: Lists specific user IDs processed
- **No Data**: Logs when no accounts need deletion
- **Errors**: Detailed error messages and stack traces
- **Missing Tables**: Informative messages about requirements

## Integration Points

### Used By
- Scheduled cleanup jobs
- GDPR compliance processes
- Account lifecycle management
- Data retention policies

### External Dependencies
- **MySQL Portal**: User authentication and event data
- **MongoDB**: Account deletion records
- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging

## Compliance Features

### Data Protection
- **Retention Policy**: 90-day configurable retention period
- **Complete Removal**: Multi-system data deletion
- **Audit Trail**: Comprehensive logging of all operations
- **Status Tracking**: Prevents accidental re-processing

### Privacy Compliance
- **GDPR Right to Erasure**: Systematic data removal
- **Data Minimization**: Removes only necessary backup data
- **Retention Limits**: Automatic cleanup after retention period
- **Audit Logging**: Complete operation tracking

## Technical Details

### Date Calculation
- **Retention Period**: 90 days configurable interval
- **UTC Conversion**: Database-compatible timestamp format
- **Precise Filtering**: Millisecond-accurate date calculations

### Batch Operations
- **Efficient Queries**: Single operations for multiple users
- **Atomic Updates**: Consistent state across all systems
- **Performance Optimization**: Minimal database round trips

### Database Interactions
- **Read Operations**: Event identification and user lookup
- **Delete Operations**: Multi-table cleanup
- **Update Operations**: Status tracking for completed deletions

## Security Considerations

- **Access Control**: Limited to scheduled job execution
- **Data Validation**: Verifies user IDs before deletion
- **Audit Logging**: Complete operation tracking
- **Error Isolation**: Failures don't affect other operations

## Performance Considerations

- **Batch Processing**: Handles multiple deletions efficiently
- **Index Usage**: Optimized queries on indexed columns
- **Connection Pooling**: Efficient database resource usage
- **Memory Management**: Minimal memory footprint

## Usage Guidelines

1. **Scheduling**: Run as scheduled background job
2. **Monitoring**: Check logs for successful operations
3. **Error Handling**: Monitor for table existence issues
4. **Retention Policy**: Adjust 90-day period as needed
5. **Testing**: Verify cleanup in non-production environments

## Dependencies

- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging system
- **AccountDelete Model**: MongoDB document model
- **Knex.js**: SQL query builder for database operations