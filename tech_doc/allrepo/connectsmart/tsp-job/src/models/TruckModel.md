# TruckModel

## Overview
MongoDB-based model for truck mapping and logistics data in the TSP Job system. Manages truck fleet information, route mapping, and logistics optimization data for freight and delivery service integration.

## Model Definition
```javascript
const mongoose = require('mongoose');
const conn = require('@maas/core/mongo')('cache');
const tz = require('moment-timezone');
const Schema = mongoose.Schema;

const TruckMapModel = new mongoose.Schema({
  _id: {
    type: Schema.Types.ObjectId,
    required: true,
    auto: true,
  },
  truck_map: {
    type: Schema.Types.Array,
    of: Object,
    required: true,
  },
  created_at: {
    type: Date,
    required: true,
    default: tz().utc(),
  },
});

module.exports = {
  TruckMapModel: conn.model('truck_map', TruckMapModel)
}
```

## Database Configuration
- **Database**: Cache MongoDB instance
- **Collection**: `truck_map`
- **ORM**: Mongoose with structured schema
- **Connection**: Managed by @maas/core MongoDB connection
- **Timezone**: UTC with moment-timezone integration

## Purpose
- Truck fleet mapping and tracking
- Logistics route optimization
- Freight service integration
- Delivery coordination management
- Transportation network analysis

## Key Features
- Flexible truck mapping data structure
- Timestamp tracking with timezone support
- Array-based mapping information storage
- ObjectId-based unique identification
- Real-time logistics data management

## Technical Implementation
The model defines a structured schema for truck mapping data, utilizing MongoDB's flexible document structure to store complex logistics information including routes, schedules, and fleet coordination data.

### Schema Structure
```javascript
// TruckMapModel document structure
{
  _id: ObjectId,           // Unique document identifier
  truck_map: [             // Array of truck mapping objects
    {
      truck_id: "string",          // Truck identifier
      driver_id: "string",         // Assigned driver
      route_data: {},              // Route information
      schedule: {},                // Delivery schedule
      capacity: {},                // Load capacity details
      location: {},                // Current/planned locations
      status: "string",            // Operational status
      assignments: []              // Delivery assignments
    }
  ],
  created_at: Date         // Document creation timestamp
}
```

### Model Operations
```javascript
// Create new truck mapping
const { TruckMapModel } = require('./TruckModel');

const truckMapping = new TruckMapModel({
  truck_map: [
    {
      truck_id: 'TRUCK_001',
      driver_id: 'DRIVER_123',
      route_data: {
        origin: { lat: 30.2672, lng: -97.7431 },
        destination: { lat: 30.3072, lng: -97.7531 },
        waypoints: [
          { lat: 30.2772, lng: -97.7481, delivery_id: 'DEL_001' },
          { lat: 30.2872, lng: -97.7501, delivery_id: 'DEL_002' }
        ]
      },
      schedule: {
        start_time: new Date(),
        estimated_completion: new Date(Date.now() + 4 * 60 * 60 * 1000),
        delivery_windows: []
      },
      capacity: {
        max_weight: 5000,
        max_volume: 100,
        current_load: 2500
      },
      status: 'active'
    }
  ]
});
await truckMapping.save();

// Query truck mappings by status
const activeTrucks = await TruckMapModel.find({
  'truck_map.status': 'active',
  created_at: { $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
});

// Update truck location
await TruckMapModel.updateOne(
  { 'truck_map.truck_id': 'TRUCK_001' },
  { 
    $set: { 
      'truck_map.$.location.current': { lat: 30.2772, lng: -97.7481 },
      'truck_map.$.location.updated_at': new Date()
    } 
  }
);
```

## Truck Mapping Components
### Vehicle Information
- **Truck Identification**: Unique vehicle identifiers
- **Driver Assignment**: Driver-truck relationships
- **Vehicle Specifications**: Capacity, type, and capabilities
- **Operational Status**: Active, maintenance, offline states

### Route Management
- **Origin/Destination**: Trip start and end points
- **Waypoint Mapping**: Delivery stop coordinates
- **Route Optimization**: Efficient path calculation
- **Traffic Integration**: Real-time route adjustments

### Scheduling System
- **Time Windows**: Delivery time constraints
- **Schedule Optimization**: Efficient delivery sequencing
- **Real-time Adjustments**: Dynamic schedule updates
- **Delay Management**: Schedule deviation handling

### Capacity Management
- **Load Tracking**: Current cargo information
- **Weight Limits**: Vehicle capacity constraints
- **Volume Optimization**: Space utilization efficiency
- **Multi-stop Planning**: Capacity across deliveries

## Integration Points
- **TruckService**: Business logic and operations
- **Route Optimization**: Path planning algorithms
- **Delivery Management**: Package and freight coordination
- **Fleet Tracking**: Real-time vehicle monitoring
- **Analytics Services**: Performance and efficiency metrics

## Usage Context
Critical for:
- Fleet management operations
- Delivery route optimization
- Logistics coordination
- Real-time truck tracking
- Capacity planning and utilization
- Performance analytics and reporting

## Performance Considerations
- MongoDB indexing for efficient truck queries
- Real-time location update optimization
- Batch processing for route calculations
- Caching of frequently accessed truck data
- Scalable document structure for large fleets

### Indexing Strategy
```javascript
// Recommended indexes for performance
db.truck_map.createIndex({ "truck_map.truck_id": 1 });
db.truck_map.createIndex({ "truck_map.status": 1 });
db.truck_map.createIndex({ "truck_map.driver_id": 1 });
db.truck_map.createIndex({ created_at: -1 });
db.truck_map.createIndex({ "truck_map.location.current": "2dsphere" });
```

## Timezone Management
The model incorporates moment-timezone for accurate timestamp handling:
- UTC-based timestamp storage
- Timezone conversion capabilities
- Regional time zone support
- Scheduling coordination across time zones

## Security Features
- Secure truck data access control
- Driver privacy protection
- Route information security
- Real-time tracking data protection
- Audit logging for truck operations

## Related Models
- TruckService: Business logic implementation
- Trips: Integration with passenger services
- AuthUsers: Driver account management
- Reservations: Coordination with passenger bookings
- Analytics models: Performance tracking

## API Integration
Essential for:
- Fleet management endpoints
- Real-time tracking services
- Route optimization APIs
- Delivery coordination systems
- Performance monitoring dashboards

## Business Logic Support
### Route Optimization
- Multi-stop delivery planning
- Traffic-aware routing
- Fuel efficiency optimization
- Time window compliance
- Dynamic route adjustments

### Fleet Management
- Vehicle assignment algorithms
- Driver scheduling optimization
- Maintenance coordination
- Capacity utilization tracking
- Performance monitoring

## Development Notes
- Designed for real-time fleet operations
- Supports complex logistics workflows
- Compatible with mapping services integration
- Optimized for high-frequency updates
- Follows microservices architecture patterns

## Analytics and Reporting
- Fleet utilization metrics
- Route efficiency analysis
- Driver performance tracking
- Delivery success rates
- Cost optimization insights

## Data Quality Management
- Location data validation
- Route consistency verification
- Schedule accuracy monitoring
- Capacity constraint enforcement
- Real-time data synchronization

## Scalability Considerations
- MongoDB horizontal scaling support
- Efficient geo-spatial queries
- Real-time data processing
- Distributed fleet management
- Load balancing for tracking services

## Monitoring and Maintenance
- Real-time fleet monitoring
- Performance metric tracking
- System health monitoring
- Data integrity verification
- Operational efficiency analysis

## Integration Capabilities
- GPS tracking systems
- Route planning services
- Delivery management platforms
- Fleet telematics integration
- Business intelligence tools

## Operational Features
- Real-time location tracking
- Dynamic route optimization
- Automated dispatch coordination
- Performance analytics
- Maintenance scheduling integration