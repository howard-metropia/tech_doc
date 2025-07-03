# PIMA Service

## Overview

The PIMA service manages data synchronization for Pima County government employees, handling user registration, trip data, and reservation information from the enterprise portal to analytics databases with timezone conversion and data validation.

## Service Information

- **Service Name**: PIMA
- **File Path**: `/src/services/pima.js`
- **Type**: Enterprise Data Management Service
- **Dependencies**: Moment.js, InfluxDB, MySQL, Data Models

## Configuration

### PIMA Domains
```javascript
const PIMA_DOMAINS = [
  'pima.gov', 'sc.pima.gov', 'pcao.pima.gov',
  'coc.pima.gov', 'pcjcc.pima.gov', 'sheriff.pima.gov'
];
```

### Exclusion Lists
- **User IDs**: [10648, 10736, 12144, 10812, 10137, 12197]
- **Email Addresses**: Specific Natalie.shepp emails across domains
- **Batch Size**: 1000 records per processing batch

### Timezone Settings
- **Target Timezone**: US/Mountain for local time conversion
- **Date Format**: YYYY-MM-DD HH:mm:ss for database storage

## Functions

### writeUsers()

Synchronizes PIMA enterprise users to analytics database.

**Purpose**: Migrates verified enterprise users for analytics and reporting
**Parameters**: None (processes enterprise members)
**Returns**: Promise (async function)

**Data Processing**:
- Joins enterprise and auth_user tables
- Filters by PIMA government domains
- Excludes specific test users and emails
- Groups by user_id to handle duplicate enterprise emails
- Converts UTC timestamps to Mountain timezone

**User Data Fields**:
- **UserID**: Hashed user identifier
- **Enterprise Info**: Email, domain, verification status
- **Personal Info**: First name, last name
- **Timestamps**: Join date, verification date in local timezone
- **Email Verification**: Success/Not Verified status

### writeReservations(start, end)

Synchronizes carpool reservation data for PIMA users.

**Purpose**: Tracks carpool reservations and matching statistics
**Parameters**:
- `start` (string): Start date filter (optional, defaults to last record or 2023-04-01)
- `end` (string): End date filter (optional, defaults to current date)

**Returns**: Promise (async function)

**Reservation Data Fields**:
- **Reservation ID**: Primary identifier
- **UserID**: Hashed user identifier
- **Coordinates**: Origin/destination latitude/longitude
- **Timing**: Start/end times in Mountain timezone
- **Travel Mode**: Carpool driver/rider classification
- **Matching**: Invite and match statistics
- **Financial**: Chip-in pricing information

### writeTrips(start, end)

Synchronizes completed trip data for PIMA users.

**Purpose**: Records actual completed carpool trips
**Parameters**:
- `start` (string): Start date filter (optional, defaults to last record or 2023-05-01)
- `end` (string): End date filter (optional, defaults to current date)

**Returns**: Promise (async function)

**Trip Data Fields**:
- **Trip ID**: Primary identifier
- **UserID**: Hashed user identifier
- **Departure Time**: Mountain timezone departure
- **Travel Mode**: Instant/regular carpool, driver/rider

## Data Processing

### User Verification
- **Email Verification**: Tracks success/not verified status
- **Domain Validation**: Ensures government domain membership
- **Duplicate Prevention**: Prevents existing user re-processing
- **Hash Generation**: Secure user ID hashing

### Date Range Processing
- **Automatic Range**: Uses last record date for incremental updates
- **Custom Range**: Supports manual date range specification
- **Timezone Conversion**: UTC to US/Mountain automatic conversion
- **Fallback Dates**: Default start dates for empty tables

### Batch Processing
- **Batch Size**: 1000 records per iteration
- **Offset Pagination**: Efficient large dataset processing
- **Duplicate Detection**: Prevents re-insertion of existing records
- **Memory Management**: Filters null results before database operations

## Travel Mode Classification

### Carpool Types
- **Regular Carpool**: travel_mode = 100
- **Instant Carpool**: travel_mode = 101
- **Role Classification**: Driver (role = 1) vs Rider (role ≠ 1)

### Mode Strings
- **carpool_driver**: Regular carpool driver
- **carpool_ride**: Regular carpool rider
- **instant_carpool_driver**: Instant carpool driver
- **instant_carpool_ride**: Instant carpool rider

## Integration Points

### Data Sources
- **Enterprise Table**: User registration and verification
- **Auth_User Table**: Personal information
- **Reservation Table**: Carpool reservations
- **Reservation_Match Table**: Matching statistics
- **Trip Table**: Completed trips

### Analytics Tables
- **pima_users**: User demographics and verification status
- **pima_reservations**: Reservation and matching data
- **pima_trip**: Completed trip records

### External Dependencies
- **InfluxDB**: Job completion metrics
- **MySQL Portal**: Source data
- **MySQL Dataset**: Target analytics database
- **Moment.js**: Date manipulation and timezone conversion

## Error Handling

### Data Validation
- **Date Validation**: Moment.js validation for date parameters
- **Domain Filtering**: Ensures PIMA government domains only
- **User Exclusion**: Filters test accounts and specific users
- **Duplicate Prevention**: Checks existing records before insertion

### Batch Processing Safety
- **Transaction Safety**: Atomic batch insertions
- **Error Isolation**: Individual record failures don't affect batch
- **Rollback Capability**: Failed batches can be retried
- **Status Tracking**: Update timestamps for resumable processing

### Monitoring
- **InfluxDB Metrics**: Success counters and job tracking
- **Comprehensive Logging**: Detailed operation logging
- **Progress Tracking**: Offset and batch completion logging
- **Performance Metrics**: Processing time and record counts

## Performance Optimization

### Database Efficiency
- **Indexed Queries**: Optimized queries on user_id and dates
- **Batch Insertions**: Efficient bulk data operations
- **Connection Pooling**: Reused database connections
- **Query Optimization**: Joins and filters optimized for performance

### Memory Management
- **Batch Size Control**: 1000 records prevent memory overflow
- **Result Filtering**: Removes null results before processing
- **Garbage Collection**: Clears arrays between iterations
- **Promise Batching**: Parallel processing with Promise.all

## Security Considerations

- **User ID Hashing**: Protects user identity in analytics
- **Domain Validation**: Ensures government employee data only
- **Exclusion Lists**: Prevents test data and specific user exposure
- **Data Isolation**: PIMA data separated from general user data

## Usage Guidelines

1. **Scheduling**: Run as scheduled ETL jobs
2. **Date Ranges**: Use incremental processing for efficiency
3. **Monitoring**: Check InfluxDB metrics for job health
4. **Error Handling**: Monitor logs for processing issues
5. **Data Validation**: Verify timezone conversions and record counts

## Dependencies

- **Moment.js**: Date manipulation and timezone conversion
- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging
- **InfluxDB Helper**: Metrics and monitoring
- **Hash Helper**: Secure user ID hashing