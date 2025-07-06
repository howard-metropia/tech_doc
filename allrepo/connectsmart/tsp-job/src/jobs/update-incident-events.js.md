# update-incident-events.js

## Overview
Complex job module responsible for processing traffic incident events, analyzing their impact on user trips, and sending intelligent notifications to affected users. This comprehensive system manages the entire lifecycle of incident event processing from detection to user notification, including polygon intersection analysis, ETA calculations, and user preference filtering.

## Purpose
- Process and update traffic incident events from external data sources
- Analyze incident impact on various trip types (habitual, reservation, calendar, carpool)
- Send targeted notifications to users whose trips may be affected
- Maintain incident event cache and historical records
- Provide real-time traffic intelligence and route optimization

## Key Features
- **Multi-Trip Analysis**: Supports habitual, reservation, calendar, and carpool trips
- **Intelligent Notifications**: Context-aware notifications based on trip type and user preferences
- **Polygon Intersection**: Advanced geospatial analysis for trip-incident overlap
- **ETA Calculations**: Real-time estimated time of arrival impact assessment
- **Schema Validation**: Comprehensive data validation for incident, flood, and closure events
- **Regional Tagging**: Automatic geographic region classification (zipcode, city, county)
- **Metrics Collection**: Performance and usage analytics via InfluxDB

## Dependencies
```javascript
const config = require('config');
const { logger } = require('@maas/core/log');
const EventAggregator = require('@app/src/models/EventAggregator');
const IncidentsEvent = require('@app/src/models/IncidentsEvent');
const TripTrajectoryBuffering = require('@app/src/models/TripTrajectoryBuffering');
const TripTrajectoryIndex = require('@app/src/models/TripTrajectoryIndex');
const CalendarEvents = require('@app/src/models/CalendarEvents');
const NotificationRecord = require('@app/src/models/NotificationRecord');
const UISTestLog = require('@app/src/models/UISTestLog');
const { sendNotification } = require('@app/src/services/sendNotification');
const { hereRouting } = require('@app/src/services/hereAPI');
const knex = require('@maas/core/mysql')('portal');
const moment = require('moment-timezone');
const { AlertManager } = require('@maas/services');
const { IncidentSchemas, FloodSchemas, ClosureSchemas } = require('@app/src/schemas/uisSchema');
const poly = require('@app/src/services/hereMapPolylines');
const turf = require('@turf/turf');
const { v4: uuidv4 } = require('uuid');
const ReservationPolyline = require('@app/src/models/ReservationPolyline');
const ZipcodeGeometry = require('@app/src/models/ZipcodeGeometry');
const CityCodeGeometry = require('@app/src/models/CityCodeGeometry');
const CountyCodeGeometry = require('@app/src/models/CountyCodeGeometry');
const { InfluxDB, Point } = require('@influxdata/influxdb-client');
```

## Core Function Structure
```javascript
module.exports = {
  inputs: {},
  fn: async function () {
    // Main execution flow
    // 1. Fetch and validate incident events
    // 2. Analyze trip impacts
    // 3. Send notifications
    // 4. Update cache and metrics
  }
};
```

## Processing Architecture

### Main Execution Flow
1. **Event Fetching**: Retrieve ongoing events from EventAggregator and cache
2. **Schema Validation**: Validate events against incident, flood, and closure schemas
3. **Event Classification**: Identify new, updated, and closed events
4. **Trip Analysis**: Analyze impact on different trip types
5. **User Filtering**: Apply user preference and toggle settings
6. **Polygon Intersection**: Perform geospatial analysis for trip-incident overlap
7. **ETA Calculation**: Calculate estimated time impact for affected trips
8. **Notification Processing**: Send contextual notifications to affected users
9. **Cache Update**: Update incident event cache in MongoDB
10. **Metrics Recording**: Log performance and usage metrics to InfluxDB

## Event Data Sources

### EventAggregator Model
```javascript
const fetchOngoingEventFromAggregator = async (nowTime) => {
  const result = await EventAggregator.find({
    expires: { $gte: nowTime }
  }).select({
    description: 1, event_id: 1, location: 1, record_formatted: 1,
    type: 1, lat: 1, lon: 1, polygon: 1, start: 1, expires: 1,
    version: 1, reroute: 1
  }).lean();
  return result;
};
```

### Incident Event Cache
```javascript
const fetchOngoingEventFromCache = async () => {
  const result = await IncidentsEvent.find({ close: false }).lean();
  return result;
};
```

## Schema Validation System

### Supported Event Types
- **Incident**: General traffic incidents (accidents, stalls, debris)
- **Flood**: Weather-related flooding events
- **Closure**: Construction zones and road closures

### Validation Process
```javascript
const checkSchema = async (curEvent) => {
  const validEventList = [];
  curEvent.forEach(async (event) => {
    if (event.type === 'incident') {
      const validResult = await IncidentSchemas.validateAsync(event);
      validEventList.push(validResult);
    } else if (event.type === 'Flood') {
      const validResult = await FloodSchemas.validateAsync(event);
      validEventList.push(validResult);
    } else if (event.type === 'Closure') {
      const validResult = await ClosureSchemas.validateAsync(event);
      validEventList.push(validResult);
    }
  });
  return validEventList;
};
```

## Trip Analysis System

### Habitual Trip Processing
```javascript
const checkHabitualTrip = async (startTime, closeTime, nowTime) => {
  // Complex SQL query analyzing user travel patterns
  // Considers weekday/weekend patterns, time slots, probabilities
  // Filters for high-confidence trips with recent activity
  // Returns trips likely to be affected by incident timing
};
```

### Reservation Trip Analysis
```javascript
const checkReservationTrip = async (startTime, closeTime, nowTime) => {
  // Query confirmed reservations within incident timeframe
  // Filters for car travel mode and confirmed status
  // Includes 30-minute notification window
  // Returns active reservations potentially affected
};
```

### Calendar Event Integration
```javascript
const checkCalendarTrip = async (startTime, closeTime, nowTime, eventId) => {
  // MongoDB query for calendar events with reminders
  // Filters for events within incident timeframe
  // Excludes removed events
  // Includes 30-minute notification buffer
};
```

### Carpool Trip Support
```javascript
const checkCarpoolTrip = async (startTime, closeTime, nowTime) => {
  // Currently returns empty array - feature disabled
  // Architecture supports future carpool integration
  // Would analyze duo reservations and matched trips
};
```

## Geospatial Analysis Engine

### Polygon Intersection Analysis
```javascript
const findIntersectedHTrip = async (eventId, nowTime, tripList, eventPolygon) => {
  // MongoDB geospatial query using $geoIntersects
  // Analyzes trip trajectories against incident polygons
  // Supports both buffered and original trajectory modes
  // Returns trips with spatial overlap
};
```

### Route Polyline Analysis
```javascript
const checkPolyMatch = async (o, d, eventPolygon, eventId, tripType) => {
  // Uses HERE Routing API to generate trip polylines
  // Decodes polylines and converts to GeoJSON
  // Performs turf.js intersection analysis
  // Returns boolean match result
};
```

## User Preference System

### Toggle Settings Integration
```javascript
const checkToggleSetting = async (candidateTrip, type) => {
  // Queries user notification preferences
  // Filters trips based on user toggle settings
  // Supports incident, flood, and construction notifications
  // Returns only trips where user has enabled notifications
};

const toggleSettingTypeMappingTable = [
  { event_type: 'incident', toggle_type: 'road_incident' },
  { event_type: 'Flood', toggle_type: 'flood_warning' },
  { event_type: 'Closure', toggle_type: 'construction_zone' },
  { event_type: 'TransitIncident', toggle_type: 'transit_incident' }
];
```

## ETA Impact Assessment

### Real-Time ETA Calculation
```javascript
const calculateETA = async (candidateTrip, nowTime, eventId) => {
  // Gets user current location from app_data table
  // Calculates route to trip origin using HERE API
  // Compares ETA with trip departure time
  // Sets ETACheck flag (1=affected, 0=not affected, -1=error)
};
```

### Performance Optimization
- Efficient API calls to HERE Routing service
- Caching of user location data
- Optimized database queries for trip analysis
- Parallel processing of multiple trip calculations

## Notification System

### Notification Types
- **Type 92**: Incident detection notifications
- **Type 93**: Incident cleared notifications

### Context-Aware Messaging
```javascript
const getNotificationTitle = (event) => {
  // Generates context-specific notification titles
  // Includes emoji indicators for visual appeal
  // Differentiates between detection and clearance
  // Considers event type (incident, flood, closure)
};

const getNotificationBody = (event, tripType) => {
  // Creates detailed notification messages
  // Customizes wording based on trip type
  // Includes roadway names when available
  // Provides actionable information for users
};
```

### Trip Type Customization
- **Habitual**: "on one of your frequent trips"
- **Reservation**: "on your upcoming trip"
- **Calendar**: "on your upcoming calendar event trip"
- **Carpool**: "on your upcoming carpool trip"

## Regional Geographic Tagging

### Automatic Region Detection
```javascript
const getRegionCode = async (event) => {
  const zipCode = await getZipCode(event.lat, event.lon);
  const cityCode = await getCityCode(event.lat, event.lon);
  const countyCode = await getCountyCode(event.lat, event.lon);
  return { zipcode_tag: zipCode, city_tag: cityCode, county_tag: countyCode };
};
```

### Geospatial Queries
- Uses MongoDB geospatial indexes for efficient lookups
- Performs point-in-polygon analysis with turf.js
- Supports multi-polygon geometries for complex regions
- Provides fallback handling for unmatched locations

## Performance Metrics and Analytics

### InfluxDB Integration
```javascript
const influxData = {
  measurement: 'event_trip_matching_count',
  tags: { project: process.env.PROJECT_NAME, stage: process.env.PROJECT_STAGE },
  fields: {
    input_habitual_trip: Number(hTripCount),
    input_reservation_trip: Number(rTripCount),
    input_calendar_trip: Number(cTripCount),
    time_matched_trip: Number(tMatchedTCount),
    area_matched_trip: Number(aMatchedTCount),
    execution_duration: Number(executionDuration),
    event_id: `${event.event_id}T${nowTime}`
  }
};
```

### Performance Tracking
- Trip analysis execution duration
- Notification sending success rates
- Database query performance metrics
- API call response times

## Error Handling and Monitoring

### Comprehensive Error Management
```javascript
try {
  // Main processing logic
} catch (e) {
  const alert = new AlertManager(slackConfig);
  const alertMessage = {
    project: 'tsp-job',
    stage: process.env.PROJECT_STAGE,
    status: 'ERROR',
    vendor: 'update-incident-event',
    originApi: 'tsp-job job : update-incident-events',
    errorMsg: `UIS batch job failed ${nowTime}: ${JSON.stringify(e.message)}`,
    meta: `UIS batch job failed ${nowTime}`
  };
  alert.sendMsg(alertMessage);
}
```

### Slack Integration
- Real-time error alerting via Slack
- Structured error messages with context
- Integration with AlertManager service
- Environment-specific alert routing

## Data Persistence

### MongoDB Collections
- **IncidentsEvent**: Main incident cache with user impact data
- **NotificationRecord**: Comprehensive notification history
- **UISTestLog**: Test event logging for debugging

### Database Operations
```javascript
await IncidentsEvent.updateOne(
  { event_id: event.event_id },
  {
    event_id: event.event_id,
    description: event.description,
    location: event.location,
    type: event.type,
    incident_type: event.incident_type,
    polygon: event.polygon,
    affected_users: event.affected_users,
    close: event.close
  },
  { upsert: true }
);
```

## Configuration Management

### Environment Configuration
- Slack webhook configurations
- Database connection settings
- HERE API credentials and endpoints
- InfluxDB connection parameters
- Habitual trip intersection mode settings

### Feature Flags
- `habitualTripIntersectionMode`: Controls trajectory analysis method
- Event type processing toggles
- Notification sending controls

## Testing and Debugging

### Test Event Support
```javascript
if (eventId.includes('TEST')) {
  await recordTestLog(eventId, nowTime, `candidateHTrip: ${JSON.stringify(candidateHTrip)}`);
}
```

### Comprehensive Logging
- Detailed process flow logging
- Trip analysis step-by-step tracking
- Performance measurement logging
- Error context preservation

## Security Considerations
- Secure API key management for external services
- Database access control and authentication
- User data privacy protection during processing
- Audit trails for notification sending

## Scalability Features
- Parallel processing of multiple events
- Efficient database queries with proper indexing
- Memory-optimized data structures
- Horizontal scaling support

## Integration Points
- **EventAggregator**: Primary data source for incident events
- **HERE Maps API**: Routing and polyline services
- **Notification Service**: User notification delivery
- **InfluxDB**: Performance metrics and analytics
- **Slack**: Error alerting and monitoring
- **MongoDB**: Data persistence and caching
- **MySQL**: User and trip data access

## Deployment Considerations
- Requires multiple external service connections
- Database performance optimization needed
- Memory and CPU resource planning
- Network latency considerations for API calls

## Future Enhancements
- Enhanced machine learning for trip prediction
- Advanced notification personalization
- Real-time streaming event processing
- Improved geospatial analysis algorithms
- Multi-modal transportation support
- Enhanced analytics and reporting capabilities