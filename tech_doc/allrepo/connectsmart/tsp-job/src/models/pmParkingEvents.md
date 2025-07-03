# pmParkingEvents Model Documentation

## Overview
PmParkingEvents is a Mongoose-based model that provides high-performance caching for ParkMobile parking event data in MongoDB. This model serves as a caching layer for frequently accessed parking events and API response data.

## Schema Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('dataset');

const mongoSchema = new Schema({
  _id: { type: String },
  card: { type: String },
  http_status: { type: Number || String },
  response: { type: Object },
}, { timestamps: true });

const PmParkingEvents = conn.model('pm_parking_events', mongoSchema);
```

## Database Configuration
- **Database**: Dataset MongoDB (`dataset`)
- **Collection**: `pm_parking_events`
- **ORM**: Mongoose ODM
- **Connection**: Managed through @maas/core/mongo
- **Purpose**: High-performance event data caching

## Schema Structure

### Core Fields
- **_id**: Unique event identifier (String)
- **card**: Payment card reference or identifier
- **http_status**: HTTP response status from ParkMobile API
- **response**: Complete API response object storage
- **timestamps**: Automatic creation and update timestamps

### Response Object
- Flexible schema for storing complete API responses
- Preserves original data structure from ParkMobile
- Supports various response formats and versions
- Enables comprehensive event data analysis

## Core Functionality

### Event Caching
- High-speed caching of ParkMobile API responses
- Reduces API call frequency and improves performance
- Stores complete event context for analysis
- Maintains data consistency across system components

### API Response Management
- Preserves original API response structure
- Tracks HTTP status codes for debugging
- Supports error response caching
- Enables response pattern analysis

## Usage Patterns

### Cache Operations
```javascript
const PmParkingEvents = require('./pmParkingEvents');

// Cache parking event response
const cachedEvent = await PmParkingEvents.create({
  _id: eventId,
  card: cardIdentifier,
  http_status: 200,
  response: {
    event_type: 'parking_start',
    zone_id: 'ZONE_123',
    session_data: sessionInfo,
    timestamp: new Date(),
    status: 'success'
  }
});

// Retrieve cached event
const eventData = await PmParkingEvents.findById(eventId);

// Query events by card
const cardEvents = await PmParkingEvents.find({ card: cardId })
  .sort({ createdAt: -1 })
  .limit(50);
```

### Performance Optimization
- Fast retrieval of frequently accessed events
- Reduced load on primary MySQL database
- Improved response times for mobile applications
- Bulk data processing capabilities

## Caching Strategies

### Event Type Caching
- **Session Events**: Complete parking session data
- **Payment Events**: Transaction and billing information
- **Error Events**: Failed API calls and system errors
- **Status Updates**: Real-time parking status changes

### Data Lifecycle Management
- **Fresh Data**: Recently cached events with high access frequency
- **Warm Data**: Moderately accessed historical events
- **Cold Data**: Archived events for compliance and analysis
- **Expired Data**: Automatic cleanup of outdated cache entries

## Integration Points

### ParkMobile API
- **Response Caching**: API response storage
- **Error Handling**: Failed request caching
- **Rate Limiting**: API call optimization
- **Data Validation**: Response format verification

### Internal Systems
- **pmParkingEvent**: Primary storage correlation
- **Analytics Engine**: Cached data analysis
- **Mobile Applications**: Fast data serving
- **Reporting Systems**: Historical data access

## Performance Features

### Query Optimization
- Efficient indexing on frequently queried fields
- Optimized aggregation pipelines
- Memory-efficient data structures
- Connection pooling and management

### Scalability
- Horizontal scaling support
- Sharding capabilities for large datasets
- Load balancing across MongoDB replicas
- Automatic failover mechanisms

## Data Integrity

### Consistency Management
- Primary-cache synchronization
- Conflict resolution strategies
- Data validation and verification
- Eventual consistency guarantees

### Error Handling
- Graceful degradation on cache misses
- Automatic cache refresh mechanisms
- Error response preservation
- Fallback to primary data sources

## Security Considerations
- Secure MongoDB connection handling
- Access control and authentication
- Data encryption for sensitive fields
- Network security and isolation

## Monitoring and Maintenance

### Cache Performance Monitoring
- Cache hit/miss ratio tracking
- Response time metrics
- Storage utilization monitoring
- Query performance analysis

### Maintenance Operations
- Regular cache cleanup and optimization
- Index maintenance and rebuilding
- Data consistency validation
- Performance tuning and optimization

## Analytics Capabilities
- Event pattern analysis
- API performance monitoring
- User behavior insights
- System health metrics

## Related Components
- **pmParkingEvent**: Primary event storage
- **pmPriceObjects**: Pricing data caching
- **Cache Management Jobs**: Automated maintenance
- **Analytics Dashboard**: Performance visualization

## Future Enhancements
- Real-time event streaming
- Advanced caching algorithms
- Machine learning-based cache optimization
- Multi-region cache replication
- Enhanced analytics capabilities