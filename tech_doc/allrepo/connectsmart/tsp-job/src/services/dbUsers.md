# Database Users Service

## Overview

The Database Users service manages user data synchronization between authentication tables and analytics databases, handling timezone calculations, user data migration, and maintaining user records for analytics purposes.

## Service Information

- **Service Name**: Database Users
- **File Path**: `/src/services/dbUsers.js`
- **Type**: Data Management Service
- **Dependencies**: Moment.js, Geo-TZ, InfluxDB, MySQL

## Functions

### setUserTimezone()

Updates user timezone information based on registration coordinates.

**Purpose**: Calculates and sets timezone for users based on their registration location
**Parameters**: None (processes users from database)
**Returns**: Promise (async function)

**Process Flow**:
1. Queries users with lat/lng but no timezone
2. Validates coordinate ranges (-90 to 90 lat, -180 to 180 lng)
3. Uses geo-tz library to determine timezone
4. Updates user records with calculated timezone
5. Logs metrics to InfluxDB

**Example**:
```javascript
await setUserTimezone();
// Updates users with registration coordinates but missing timezone
// Logs: "Update 150 user timezone"
```

### writeDBUser()

Migrates user data from authentication tables to analytics database.

**Purpose**: Synchronizes user data for analytics and reporting purposes
**Parameters**: None (batch processes users)
**Returns**: Promise (async function)

**Data Processing**:
- **Batch Size**: 1000 users per iteration
- **Date Filter**: Users created after 2021-06-01
- **Region Filter**: America timezone users only
- **Debug Filter**: Excludes debug users

**User Data Fields**:
- **UserID**: Hashed user identifier
- **Date**: Original creation timestamp
- **DateLocal**: Local timezone creation time
- **RegisterLon/RegisterLat**: Registration coordinates
- **Device**: iOS/Android detection
- **PromotionCode**: Registration promotion code
- **Email Fields**: Common, Facebook, Google, Apple emails

### isInDBUser(userId)

Checks if user already exists in analytics database.

**Purpose**: Prevents duplicate user records during migration
**Parameters**:
- `userId` (number): User ID to check
**Returns**: Database record or null

**Example**:
```javascript
const exists = await isInDBUser(12345);
if (!exists) {
  // User not in DB, proceed with migration
}
```

## Data Sources

### AuthUsers Table
- **Fields**: Registration data, coordinates, timezone, device info
- **Filters**: Non-debug users with valid email addresses
- **Joins**: Registration codes for promotion tracking

### Target Database
- **Table**: DBUsers (analytics database)
- **Purpose**: Reporting and analytics queries
- **Partitioning**: By date for performance

## Data Validation

### Coordinate Validation
- **Latitude**: -90 to 90 degrees
- **Longitude**: -180 to 180 degrees
- **Non-zero**: Excludes (0,0) coordinates

### Email Validation
- Requires at least one email type:
  - Common email
  - Facebook email
  - Google email
  - Apple email

### Device Detection
- **iOS**: Device model contains "iP"
- **Android**: All other devices
- **Default**: "N/A" for unknown devices

## Integration Points

### Used By
- Analytics and reporting systems
- User behavior analysis
- Geographic distribution analysis
- Device usage statistics

### External Dependencies
- **Geo-TZ**: Timezone calculation by coordinates
- **InfluxDB**: Metrics and job monitoring
- **MySQL**: Source and target databases
- **Moment.js**: Date/time manipulation

## Performance Optimization

### Batch Processing
- 1000 user batches to manage memory
- Offset-based pagination for large datasets
- Parallel processing with Promise.all

### Database Efficiency
- Binary UserID comparison for exact matches
- Indexed queries on registration coordinates
- Left joins for optional registration codes

### Memory Management
- Filters null results before database operations
- Clears batch arrays between iterations
- Garbage collection friendly patterns

## Error Handling

### Geographic Errors
- Logs invalid coordinates with user ID
- Continues processing other users
- Tracks failed vs successful updates

### Database Errors
- Duplicate prevention through existence checks
- Transaction safety for batch inserts
- Rollback capability for failed batches

### Monitoring
- InfluxDB metrics for job completion
- Success/failure counters
- Processing time tracking

## Timezone Processing

### Supported Regions
- **Primary**: America timezone zones
- **Detection**: Automatic by coordinates
- **Format**: Standard timezone identifiers (e.g., "America/Chicago")

### Local Time Conversion
- Converts UTC creation time to local timezone
- Uses moment-timezone for accurate conversion
- Handles daylight saving time transitions

## Security Considerations

- **User ID Hashing**: Protects user identity in analytics
- **Email Privacy**: Separate fields for different email types
- **Debug Exclusion**: Prevents test data pollution
- **Coordinate Validation**: Prevents injection attacks

## Usage Guidelines

1. **Timezone Updates**: Run regularly for new users
2. **Data Migration**: Schedule during low-traffic periods
3. **Monitoring**: Check InfluxDB metrics for job health
4. **Validation**: Verify coordinate ranges before processing
5. **Batch Size**: Adjust based on available memory

## Dependencies

- **Moment.js**: Date/time manipulation and timezone conversion
- **Geo-TZ**: Geographic timezone calculation
- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging
- **InfluxDB**: Metrics and monitoring storage