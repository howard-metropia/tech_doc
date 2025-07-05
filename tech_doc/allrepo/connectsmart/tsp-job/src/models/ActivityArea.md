# ActivityArea Model

## Overview
Activity area management model for the TSP Job system. Defines geographic zones and regions for activity tracking, service boundaries, and location-based features.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class ActivityArea extends Model {
  static get tableName() {
    return 'activity_area';
  }
}
module.exports = ActivityArea.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `activity_area`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Geographic zone definition
- Service area boundaries
- Activity region tracking
- Location-based service management

## Area Types
- **Service Zones**: Transportation service boundaries
- **Activity Regions**: High-activity geographic areas
- **Geofenced Areas**: Restricted or special zones
- **Commercial Districts**: Business and shopping areas
- **Residential Zones**: Housing and community areas

## Key Features
- Polygon-based area definition
- Hierarchical zone management
- Real-time geofencing capabilities
- Multi-level area classification

## Integration Points
- **CmActivityLocation**: Activity-location relationships
- **CmLocation**: Location management
- **Trips**: Trip-area associations
- **TripTrajectory**: Route-area intersections

## Usage Context
Used for service area management, activity tracking, geofencing, location-based analytics, and regional service optimization.

## Geographic Features
- Boundary polygon storage
- Spatial relationship management
- Area overlap detection
- Distance and proximity calculations

## Business Applications
- Service availability determination
- Pricing zone management
- Activity density analysis
- Regional demand forecasting

## Performance Optimization
- Spatial indexing for fast queries
- Efficient area intersection tests
- Cached boundary calculations
- Optimized for location-based operations

## Related Models
- CmActivityLocation: Activity associations
- CmLocation: Location data
- Trips: Geographic trip analysis
- TripTrajectory: Route-area relationships

## API Integration
- Geofencing services
- Area management endpoints
- Location-based query APIs
- Regional analytics services

## Analytics Support
- Activity density metrics
- Regional usage patterns
- Service coverage analysis
- Demand distribution insights

## Development Notes
- Spatial data intensive
- Real-time geofencing requirements
- Critical for location-based services
- Supports complex geographic operations