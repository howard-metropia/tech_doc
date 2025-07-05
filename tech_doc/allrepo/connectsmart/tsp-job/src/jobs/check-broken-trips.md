# Check Broken Trips Job

## Overview
Job that analyzes trip data to identify broken or problematic trips, including trips that didn't end properly and suspiciously short trips with duplicate destinations.

## File Location
`/src/jobs/check-broken-trips.js`

## Dependencies
- `ejs` - Template engine for HTML email generation
- `moment-timezone` - Date/time manipulation
- `@maas/core/log` - Logging framework
- `@app/src/helpers/mailer` - Email sending service
- `@app/src/models/Trips` - Trip data model
- `@app/src/models/AuthUsers` - User authentication model

## Job Configuration

### Inputs
```javascript
inputs: {
  assignStartDate: String,  // Optional start date for analysis
  assignEndDate: String     // Optional end date for analysis
}
```

### Email Recipients
```javascript
const receivers = [
  'henry.wang@metropia.com',
  'sibu.wang@metropia.com',
  'daniel.feng@metropia.com',
  'desmond.li@metropia.com',
  'chihhan.lin@metropia.com',
  'edward.huang@metropia.com',
  'soros.jhou@metropia.com',
  'berby.huang@metropia.com'
];
```

## Navigation App Mapping
```javascript
const NAVIGATION_APPS = {
  1: 'here',
  2: 'google', 
  3: 'apple',
  4: 'waze'
};
```

## Core Analysis Functions

### 1. listNotEndTrips()
**Purpose**: Identifies trips that never ended properly
```javascript
const similarTrip = await Trips.query()
  .where('user_id', trip.user_id)
  .andWhere((builder) => {
    builder.where('destination', trip.destination)
      .orWhere((builder) => {
        builder.where('destination_latitude', trip.destination_latitude)
          .andWhere('destination_longitude', trip.destination_longitude);
      });
  })
  .andWhereNot('ended_on', null)
```

**Logic**:
- Finds trips without end times
- Searches for similar completed trips by same user
- Matches by destination address or coordinates
- Time window: ±30 minutes from start time

### 2. listShortEndTrips()
**Purpose**: Identifies suspiciously short trips with duplicate destinations

**Analysis Process**:
1. **Group by User**: Groups all trips by user ID
2. **Filter Users**: Only processes users with multiple trips
3. **Find Similar Trips**: Identifies trips with:
   - Same destination (address or coordinates)
   - Duration < 120 seconds between end and start times
   - Different trip IDs

**Similarity Logic**:
```javascript
const duration = Math.abs(moment(trip.ended_on).diff(t.started_on, 'seconds'));
return (
  t.id !== trip.id &&
  (t.destination === trip.destination ||
    (t.destination_latitude === trip.destination_latitude &&
     t.destination_longitude === trip.destination_longitude)) &&
  duration < 120
);
```

## Date Range Handling
```javascript
const startDate = isValidStartDate
  ? moment.utc(assignStartDate).startOf('day').toISOString()
  : moment.utc().subtract(1, 'd').startOf('day').toISOString();
```

- **Default**: Previous day if no dates provided
- **Custom**: Uses provided start/end dates
- **Format**: Full day ranges (00:00:00 to 23:59:59)

## Report Generation

### HTML Email Template
- **Template**: `src/static/templates/check-broken-trips.ejs`
- **Format**: HTML email with trip details table
- **Data Include**:
  - Trip ID and user ID
  - Origin and destination details
  - Trip timing information
  - Navigation app used
  - Device platform (iOS/Android)

### Trip Data Structure
```javascript
{
  tripNumber: `Short Trip #${index}`,
  tripStatus: 'UNEXPECTED: Short trip with Same D',
  tripId: trip.id,
  userId: trip.user_id,
  originAddress: trip.origin,
  destinationAddress: trip.destination,
  startedOn: trip.started_on,
  endedOn: trip.ended_on || 'NULL',
  navigationApp: NAVIGATION_APPS[trip.navigation_app],
  device: user.device_model.includes('iPhone') ? 'iOS' : 'Android'
}
```

## Filter Logic

### Debug User Exclusion
```javascript
if (!user.is_debug) {
  tripsData.push(tripData);
}
```
Excludes trips from debug/test users from reports.

### Duplicate Prevention
- Tracks processed trip IDs to prevent duplicate reporting
- Ensures each problematic trip pair is only reported once

## Email Report Content
- **Subject**: Includes project name, stage, and date range
- **Statistics**: Total trips analyzed and problem ratio
- **Details**: Comprehensive trip information table
- **Format**: HTML email for better readability

## Performance Considerations
- Processes trips in batches to avoid memory issues
- Uses efficient database queries with proper indexing
- Filters debug users to focus on real user issues

## Error Detection Patterns
1. **Never-Ending Trips**: Trips without end timestamps
2. **Duplicate Short Trips**: Multiple quick trips to same destination
3. **Navigation Issues**: Trips with inconsistent navigation data

## Related Components
- Trip management system
- Email notification infrastructure
- Trip validation services
- Data quality monitoring system

## Schedule Context
Typically scheduled to run daily to monitor trip data quality and alert development team to potential issues.