# IncidentsEvent Model

## Overview
Incident event cache model for the TSP Job system. Provides high-performance caching layer for processed incident events, enabling rapid access to active transportation disruptions, traffic incidents, and real-time event data for user notification and trip impact analysis.

## Model Definition
```javascript
const mongoose = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const schema = new mongoose.Schema({ _id: String }, { strict: false });
const IncidentsEvent = conn.model('incidents_event', schema);

module.exports = IncidentsEvent;
```

## Database Configuration
- **Database**: Cache MongoDB instance
- **Collection**: `incidents_event`
- **ORM**: Mongoose with dynamic schema
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Schema Mode**: Non-strict (flexible document structure)

## Purpose
- High-speed access to processed incident data
- Real-time event status tracking and management
- User notification queue processing
- Trip impact analysis and route optimization
- Event lifecycle state management

## Key Features
- **Fast Access**: Optimized cache layer for real-time queries
- **Event Status**: Active/closed event state management
- **User Impact**: Affected user tracking and notification
- **Dynamic Updates**: Real-time event modification and closure
- **Geospatial Processing**: Location-based event filtering

## Event Data Structure
Processed incident events with enhanced metadata:

```javascript
{
  _id: String,                    // Unique event identifier
  event_id: String,               // External event ID
  description: String,            // Event description
  location: String,               // Enhanced location description
  type: String,                   // Event type (incident, Flood, Closure)
  incident_type: String,          // Specific incident classification
  polygon: Array,                 // Geometric boundaries
  lat: Number,                    // Latitude coordinate
  lon: Number,                    // Longitude coordinate
  record_formatted: Object,       // Structured event data
  start: Date,                    // Event start time
  expires: Date,                  // Event expiration time
  version: Array,                 // Version history tracking
  reroute: Number,                // Reroute recommendation
  region_code: Object,            // Geographic region classification
  affected_users: Array,          // Users impacted by event
  close: Boolean                  // Event closure status
}
```

## Event Status Management
Two primary states managed through the `close` field:
- **Active Events** (`close: false`): Ongoing incidents requiring monitoring
- **Closed Events** (`close: true`): Resolved incidents for notification cleanup

## Usage Context
Primary usage in the update-incident-events job for cache management:

```javascript
const fetchOngoingEventFromCache = async () => {
  try {
    const result = await IncidentsEvent.find({
      close: false,
    }).lean();
    return result;
  } catch (e) {
    logger.error(`fetchOngoingEventFromCache ${e}`);
  }
};
```

## Event Processing Pipeline
1. **Data Ingestion**: Events sourced from EventAggregator
2. **Enhancement**: Location processing and impact analysis
3. **User Matching**: Affected user identification
4. **Cache Storage**: Optimized storage in IncidentsEvent
5. **Notification**: User alert generation and delivery

## Cache Update Operations
Comprehensive upsert operations for event lifecycle management:

```javascript
await IncidentsEvent.updateOne(
  {
    event_id: event.event_id,
  }, // filter
  {
    event_id: event.event_id,
    description: event.description,
    location: event.location,
    type: event.type,
    incident_type: event.incident_type,
    polygon: event.polygon,
    lat: event.lat,
    lon: event.lon,
    record_formatted: event.record_formatted,
    start: event.start,
    expires: event.expires,
    version: event.version,
    reroute: event.reroute,
    region_code: event.region_code,
    affected_users: event.affected_users,
    close: event.close,
  }, // update
  {
    upsert: true,
  },
);
```

## Incident Type Classification
Enhanced incident categorization based on source data:
- **Vehicle Fire**: Emergency vehicle incidents
- **Hazardous Spill**: Environmental hazards
- **Crash**: Traffic accidents and collisions
- **Stalled Vehicle**: Disabled vehicle situations
- **Semi Truck Issue**: Commercial vehicle incidents
- **Bus Incident**: Public transit disruptions
- **Construction Zone**: Planned roadwork impacts
- **High Water**: Flooding conditions
- **Icy Roads**: Weather-related hazards
- **Road Debris**: Obstruction incidents

## Affected Users Tracking
Comprehensive user impact analysis:

```javascript
affected_users: [
  {
    type: 'habitual',           // Trip type classification
    trip_id: Number,            // Trip identifier
    user_id: Number,            // User identifier
    departure_time: String,     // Scheduled departure
    ETACheck: Number,           // ETA validation result
    activity_id: String,        // Activity tracking ID
    poly_match: Boolean         // Polygon intersection flag
  }
]
```

## Geographic Region Coding
Regional classification for targeted notifications:

```javascript
region_code: {
  zipcode_tag: String,          // ZIP code classification
  city_tag: String,             // City name
  county_tag: String            // County designation
}
```

## Query Patterns
- **Active Events**: `{ close: false }` for ongoing incidents
- **Event History**: Version tracking for change analysis
- **User Impact**: Affected user filtering and notification
- **Geographic Queries**: Region-based event retrieval

## Integration Points
- **EventAggregator**: Source data aggregation
- **NotificationRecord**: User alert tracking
- **TransitAlertNotificationQueue**: Alert delivery queue
- **TripTrajectoryIndex**: Route impact analysis

## Performance Optimizations
- **MongoDB Indexing**: Optimized for common query patterns
- **Lean Queries**: Memory-efficient data retrieval
- **Upsert Operations**: Efficient update-or-insert logic
- **Connection Pooling**: Managed database connections

## Cache Management Strategy
- **Real-time Updates**: Immediate cache refresh on event changes
- **Automatic Cleanup**: Expired event removal and archival
- **Memory Efficiency**: Optimized document storage and retrieval
- **Consistency**: Synchronized state with source systems

## Error Handling
Robust error management with comprehensive logging:
```javascript
try {
  // Cache operations
} catch (e) {
  logger.error(`updateCacheEvent ${e}`);
}
```

## Location Enhancement
Special processing for construction zone locations:
```javascript
location: e.type === 'Closure' 
  ? `${changeLocationOfLaneClosure(e)} (${e.description})`
  : e.location
```

## Event Closure Process
Systematic event closure with timestamp management:
```javascript
closeEvent.forEach((e) => {
  const cE = {
    ...e,
    close: true,
    incident_type: e.type === 'incident' 
      ? incidentType 
      : e.type === 'Closure' 
        ? 'Construction zone' 
        : e.type,
    location: e.type === 'Closure' 
      ? changeLocationOfLaneClosure(e) 
      : e.location,
  };
  fEvent.push(cE);
});
```

## Related Models
- EventAggregator: Source event data
- NotificationRecord: Alert delivery tracking
- TripTrajectoryBuffering: Route intersection analysis
- UISTestLog: Event processing testing and validation

## API Integration
- Real-time incident status endpoints
- User impact notification services
- Geographic event filtering
- Event lifecycle management
- Cache invalidation and refresh

## Development Notes
- Critical for real-time user notifications
- Requires high-availability cache infrastructure
- Optimized for rapid read operations
- Supports complex geospatial queries
- Essential for trip planning and route optimization