# Transit Alert Service

## Overview

The Transit Alert service manages real-time transit incident notifications for bus routes, handling both ongoing alerts and clear notifications for user favorites and active reservations.

## Service Information

- **Service Name**: Transit Alert
- **File Path**: `/src/services/transitAlert.js`
- **Type**: Transit Notification Service
- **Dependencies**: MySQL, Moment.js, Notification Models

## Core Functions

### Event Management
- **searchOngoingEvents()**: Finds active transit alerts from GTFS database
- **searchClearEvents()**: Identifies recently cleared events (within 5 minutes)
- **filterExistingNotifications()**: Prevents duplicate notifications
- **filterNotificationByUserConfig()**: Respects user notification preferences

### Route Processing
- **fetchOngoingRouteFavorites()**: Finds affected favorite routes
- **fetchOngoingReservations()**: Identifies impacted reservations
- **fetchClearFavorites()**: Processes route favorite clearances
- **fetchClearReservations()**: Handles reservation clearances

### Notification Delivery
- **notifyFavoriteRoute()**: Sends route favorite notifications
- **notifyReservation()**: Delivers reservation-specific alerts

## Notification Types

### Alert Categories
- **OngoingAlert (94)**: Active incident notifications
- **ClearAlert (95)**: Incident resolution notifications

### Affected Users
- **Route Favorites**: Users with saved favorite routes
- **Active Reservations**: Users with upcoming trips using affected routes

## Route Mapping

### Agency Mapping
```javascript
const agencyMapping = new Map([['ME', 'METRO']]);
```

### Route Number Mapping
```javascript
const routeMapping = new Map([
  [700, 'RED'], [800, 'GREEN'], 
  [900, 'PURPLE'], [433, 'SILVER']
]);
```

## Message Generation

### Title Formats
- **Ongoing**: "{Agency} Route {Number} {Effect}"
- **Clear**: "{Agency} Route {Number} is Clear Now"

### Body Content
- **Ongoing**: Uses alert header text from GTFS
- **Clear**: Standardized "route is back to normal" message

## Data Sources

### GTFS Database
- **ridemetro_transit_alert**: Main alert data
- **ridemetro_transit_alert_join_route**: Route associations

### Portal Database
- **BusRouteFavorite**: User favorite routes
- **Reservations**: Active trip reservations with transit steps
- **UserConfig**: Notification preferences
- **TransitAlertNotificationQueue**: Notification tracking

## Reservation Processing

### Trip Analysis
- Parses JSON trip steps from reservation details
- Identifies transit steps with bus mode
- Matches route IDs to affected routes
- Filters reservations starting within 30 minutes

### Step Processing
```javascript
const affectedResults = sections.map((step) => {
  if (step.type === 'transit' && step.transport?.mode === 'bus') {
    return step.transport.route_id === routeId;
  }
  return false;
});
```

## User Configuration

### Notification Filtering
- Checks user UIS settings for transit_incident preference
- Filters out notifications for users who opted out
- Logs filtered notifications for monitoring

## Metadata Structure

### Route Favorites
```javascript
{
  route_id: routeId,
  title: title,
  body: body
}
```

### Reservations
```javascript
{
  reservation_id: reservationId,
  route_id: routeId,
  origin: { lat, lon },
  destination: { lat, lon },
  started_on: isoDateTime
}
```

## Queue Management

### Notification Tracking
- **TransitAlertNotificationQueue**: Prevents duplicate notifications
- **Status Tracking**: Ongoing vs clear alert tracking
- **User Association**: Links notifications to users and routes

### Database Operations
- Inserts notification records for tracking
- Updates notification table with end times
- Manages notification lifecycle

## Error Handling

### Database Errors
- Graceful handling of query failures
- Continues processing despite individual failures
- Comprehensive error logging

### Data Validation
- Validates route ID formats
- Handles missing GTFS data
- Manages empty result sets

## Performance Optimization

### Query Efficiency
- Raw SQL for complex GTFS queries
- Efficient joins between transit and portal data
- Batch processing for notifications

### Memory Management
- Processes events in batches
- Filters unnecessary data early
- Clears arrays between operations

## Integration Points

### Used By
- Scheduled transit monitoring jobs
- Real-time alert systems
- User notification services

### External Dependencies
- **GTFS Database**: Transit alert data
- **Portal Database**: User and reservation data
- **Send Notification Service**: Message delivery
- **Moment.js**: Date/time processing

## Security Considerations

- **User Privacy**: Notification preferences respected
- **Data Access**: Controlled access to user reservations
- **Route Information**: Public transit data only

## Usage Guidelines

1. **Scheduling**: Run frequently for real-time alerts
2. **Monitoring**: Track notification delivery rates
3. **Configuration**: Verify user preference handling
4. **Testing**: Test with various route scenarios
5. **Performance**: Monitor query execution times

## Dependencies

- **MySQL**: GTFS and portal database access
- **Moment.js**: Date manipulation and formatting
- **Transit Models**: Database ORM models
- **Send Notification Service**: Message delivery
- **@maas/core/log**: Centralized logging