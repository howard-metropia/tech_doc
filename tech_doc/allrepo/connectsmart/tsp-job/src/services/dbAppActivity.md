# Database App Activity Service

## Overview

The Database App Activity service synchronizes user application activity data from portal to analytics databases, tracking user interactions, location data, and app usage patterns for behavioral analysis.

## Service Information

- **Service Name**: Database App Activity
- **File Path**: `/src/services/dbAppActivity.js`
- **Type**: User Activity Synchronization Service
- **Dependencies**: Moment.js, InfluxDB, MySQL

## Core Functions

### writeDBAppActivity(start, end)

Synchronizes application activity data to analytics database.

**Purpose**: Transfers user activity logs for behavioral analytics and usage tracking
**Parameters**:
- `start` (string): Start date filter (optional)
- `end` (string): End date filter (optional)

**Process Flow**:
1. **Date Range Calculation**: Determines synchronization period with intelligent defaults
2. **Batch Data Extraction**: Retrieves app_data records in manageable chunks
3. **Data Transformation**: Maps portal fields to analytics schema
4. **User Anonymization**: Applies hash ID transformation for privacy
5. **Batch Processing**: 1000 records per iteration for memory efficiency

## Data Sources

### AppData Table
Source table containing comprehensive user activity information:
- **User Actions**: Interaction types and behaviors
- **Location Data**: GPS coordinates and timing
- **Temporal Data**: Both GMT and local timestamps
- **Transaction Data**: Points, pricing, and ticket information

### Field Mapping
```javascript
{
  UserID: hashid(el.user_id),      // Anonymized user identifier
  userAction: el.user_action,       // Activity type
  Time: el.gmt_time,               // GMT timestamp
  TimeLocal: el.local_time,        // Local timestamp
  Lat: el.lat,                     // Latitude coordinate
  Lon: el.lon,                     // Longitude coordinate
  Email: el.email,                 // User email (if provided)
  RefID: el.ref_id,                // Reference identifier
  Thre: el.thre,                   // Threshold value
  Points: el.points,               // Earned points
  Price: el.price,                 // Transaction price
  TicketMode: el.ticket_mode,      // Ticket type mode
  TicketType: el.ticket_type,      // Specific ticket type
}
```

## Date Range Processing

### Intelligent Date Defaults
- **Empty Database**: Starts from 2020-01-01 for complete history
- **Incremental**: Uses last processed record's timestamp for continuous sync
- **Custom Range**: Supports manual date range specification
- **UTC Processing**: All date operations in UTC for consistency

### Date Logic Implementation
```javascript
if (start !== 'null' && moment(start).isValid()) {
  startDate = moment.utc(start).format('YYYY-MM-DDT00:00:00');
} else {
  const logs = await DBAppActivities.query().orderBy('id', 'desc').limit(1);
  startDate = logs.length > 0
    ? moment.utc(logs[0].created_on).format('YYYY-MM-DDT00:00:00')
    : '2020-01-01T00:00:00';
}
```

## User Activity Types

### Activity Categories
- **Navigation**: Route searches, map interactions
- **Transaction**: Ticket purchases, payment processing
- **Location**: Check-ins, location updates
- **Social**: Ratings, comments, sharing
- **System**: App launches, feature usage

### Data Elements
- **Behavioral**: User action patterns and preferences
- **Spatial**: Geographic usage and movement patterns
- **Temporal**: Usage timing and frequency
- **Financial**: Transaction and pricing data

## Privacy and Security

### User Anonymization
- **Hash ID**: Secure user identifier transformation
- **Data Minimization**: Only necessary fields transferred
- **Email Handling**: Preserves email data when explicitly provided

### Data Protection
```javascript
UserID: hashid(el.user_id),  // Converts user ID to anonymous hash
```

## Performance Optimization

### Batch Processing
- **Batch Size**: 1000 records per iteration
- **Memory Management**: Efficient large dataset handling
- **Progressive Loading**: Offset-based pagination for scalability

### Database Efficiency
- **Selective Queries**: Date-filtered record retrieval
- **Bulk Inserts**: Efficient batch database operations
- **Index Usage**: Optimized queries on created_on timestamps

## Monitoring and Metrics

### InfluxDB Integration
```javascript
const influxData = {
  measurement: 'scheduling-job',
  tags: { job: 'analytic-database' },
  fields: { successfully, sub_job: 'writeDBAppActivity' },
};
```

### Success Tracking
- **Record Count**: Number of synchronized activities
- **Processing Time**: Job execution duration
- **Throughput**: Records processed per minute

## Location Data Handling

### Geographic Information
- **Coordinates**: Precise latitude/longitude tracking
- **Location Context**: Activity-location relationships
- **Privacy Considerations**: Anonymized with user identifiers

### Spatial Analytics
- **Usage Patterns**: Geographic distribution of activities
- **Movement Analysis**: User mobility patterns
- **Service Area**: Activity concentration areas

## Error Handling

### Processing Resilience
- **Database Failures**: Comprehensive error logging
- **Data Validation**: Handles missing or invalid records
- **Transaction Safety**: Maintains data consistency

### Recovery Mechanisms
- **Incremental Restart**: Resume from last processed timestamp
- **Date Range Flexibility**: Custom range reprocessing
- **Fault Tolerance**: Continues processing despite individual record failures

## Integration Points

### Used By
- User behavior analytics
- Location-based analysis
- App usage statistics
- Product feature analytics

### External Dependencies
- **AppData Model**: Source activity data
- **DBAppActivities Model**: Target analytics table
- **InfluxDB**: Performance monitoring
- **Hash Helper**: User anonymization

## Data Quality

### Validation Features
- **Timestamp Consistency**: Ensures valid date ranges
- **Coordinate Validation**: Validates geographic data
- **Activity Classification**: Ensures proper action categorization

### Completeness Tracking
- **Record Counting**: Tracks total processed records
- **Gap Detection**: Identifies missing data periods
- **Quality Metrics**: Monitors data integrity

## Usage Guidelines

1. **Regular Sync**: Run daily for current activity data
2. **Historical Data**: Use custom date ranges for backfill
3. **Performance**: Monitor batch processing efficiency
4. **Privacy**: Ensure user anonymization compliance
5. **Storage**: Monitor analytics database growth

## Limitations

### Current Implementation
- **No Filtering**: Processes all activities without content filtering
- **Basic Validation**: Limited data quality checks
- **Simple Mapping**: Direct field-to-field transformation

### Future Enhancements
- **Activity Filtering**: Selective activity type processing
- **Data Validation**: Enhanced quality checks
- **Real-time Sync**: Near real-time activity processing

## Dependencies

- **Moment.js**: Date manipulation and formatting
- **InfluxDB Helper**: Performance metrics tracking
- **Hash Helper**: User ID anonymization
- **AppData Model**: Source activity data model
- **DBAppActivities Model**: Target analytics data model