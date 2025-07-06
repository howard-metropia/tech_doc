# EventAggregator Model

## Overview
Event data aggregation model for the TSP Job system. Handles comprehensive event ingestion, storage, and retrieval from the dataset MongoDB database for incident processing, traffic events, and real-time transportation alerts.

## Model Definition
```javascript
const mongoose = require('mongoose');
const conn = require('@maas/core/mongo')('dataset');

const schema = new mongoose.Schema({ _id: String }, { strict: false });
const EventAggregator = conn.model('event_aggregator', schema);

module.exports = EventAggregator;
```

## Database Configuration
- **Database**: Dataset MongoDB instance
- **Collection**: `event_aggregator`
- **ORM**: Mongoose with dynamic schema
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Schema Mode**: Non-strict (flexible document structure)

## Purpose
- Real-time event data aggregation from multiple sources
- Traffic incident collection and processing
- Transportation event normalization and storage
- Event lifecycle management and expiration tracking
- Geospatial event data indexing and querying

## Key Features
- **Dynamic Schema**: Flexible document structure for various event types
- **Real-time Processing**: Continuous event ingestion and updates
- **Geospatial Support**: Location-based event storage and querying
- **Expiration Management**: Event lifecycle tracking with expiration dates
- **Multi-source Integration**: Aggregates events from diverse data providers

## Event Data Structure
The model uses a non-strict schema allowing for flexible event formats:

```javascript
{
  _id: String,                    // Unique event identifier
  event_id: String,               // External event ID
  description: String,            // Event description
  location: String,               // Human-readable location
  type: String,                   // Event type (incident, Flood, Closure)
  lat: Number,                    // Latitude coordinate
  lon: Number,                    // Longitude coordinate
  polygon: Array,                 // Geometric polygon coordinates
  start: Date,                    // Event start time
  expires: Date,                  // Event expiration time
  version: Object,                // Version tracking information
  record_formatted: Object,       // Structured event data
  reroute: Number                 // Reroute recommendation flag
}
```

## Event Types
- **Traffic Incidents**: Accidents, stalled vehicles, road debris
- **Weather Events**: Flooding, icy conditions, severe weather
- **Construction Zones**: Planned roadwork and lane closures
- **Emergency Events**: Hazmat spills, vehicle fires, road closures
- **Transit Disruptions**: Public transportation service alerts

## Usage Context
Primary usage occurs in the update-incident-events job for:

```javascript
const fetchOngoingEventFromAggregator = async (nowTime) => {
  try {
    const result = await EventAggregator.find({
      expires: { $gte: nowTime },
    })
      .select({
        description: 1,
        event_id: 1,
        location: 1,
        record_formatted: 1,
        type: 1,
        lat: 1,
        lon: 1,
        polygon: 1,
        start: 1,
        expires: 1,
        version: 1,
        reroute: 1,
      })
      .lean();
    return result;
  } catch (e) {
    logger.error(`fetchOngoingEventFromAggregator ${e}`);
  }
};
```

## Query Patterns
- **Active Events**: Filter by expiration date to find ongoing events
- **Geospatial Queries**: Location-based event retrieval
- **Type Filtering**: Event categorization and type-specific processing
- **Time-based Queries**: Historical and future event analysis

## Integration Points
- **IncidentsEvent**: Cache layer for processed events
- **Notification System**: Event-driven alert generation
- **Trip Processing**: Route impact analysis and user notification
- **HERE Maps API**: Location validation and routing integration

## Data Sources
- **Traffic Management Centers**: Real-time incident feeds
- **Weather Services**: Critical weather alerts and conditions
- **Construction Databases**: Planned roadwork and closures
- **Emergency Services**: Public safety and hazmat alerts
- **Transit Agencies**: Service disruption notifications

## Performance Features
- **MongoDB Indexes**: Optimized for geospatial and temporal queries
- **Flexible Schema**: Efficient storage of varied event structures
- **Connection Pooling**: Managed database connections via @maas/core
- **Lean Queries**: Memory-efficient data retrieval

## Event Processing Workflow
1. **Ingestion**: External events aggregated into dataset collection
2. **Validation**: Schema validation against event type requirements
3. **Processing**: Event data normalized and enhanced
4. **Caching**: Processed events stored in IncidentsEvent cache
5. **Notification**: User impact analysis and alert generation

## Geospatial Capabilities
- **Polygon Storage**: Complex geometric shapes for event boundaries
- **Coordinate Indexing**: Efficient location-based queries
- **Intersection Analysis**: Route and event overlap detection
- **Buffer Zones**: Proximity-based event impact calculation

## Error Handling
Comprehensive error management with Slack alerting:
```javascript
const alert = new AlertManager(slackConfig);
const alertMessage = {
  project: 'tsp-job',
  stage: process.env.PROJECT_STAGE,
  status: 'ERROR',
  vendor: 'dataset event_aggregator',
  vendorApi: 'dataset event_aggregator',
  originApi: 'tsp-job job : update-incident-events',
  errorMsg: e.message,
  meta: 'connect dataset event_aggregator failed',
};
alert.sendMsg(alertMessage);
```

## Data Lifecycle
- **Real-time Updates**: Continuous event ingestion and modification
- **Expiration Management**: Automatic cleanup of expired events
- **Version Tracking**: Event change history and update management
- **Archive Strategy**: Historical event data retention policies

## Related Models
- IncidentsEvent: Processed event cache
- NotificationRecord: Event notification tracking
- TripTrajectoryIndex: Trip-event intersection analysis
- CalendarEvents: User schedule impact assessment

## API Integration
- Real-time event feed processing
- Geospatial query endpoints
- Event lifecycle management
- Alert generation triggers
- Data quality monitoring

## Development Notes
- Critical for real-time traffic management
- Requires robust error handling and monitoring
- Supports multiple event data formats
- Optimized for high-volume data processing
- Integration with external traffic management systems