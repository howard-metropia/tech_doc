# ReservationPolyline Model

## Overview
Reservation route polyline model for the TSP Job system. Stores geometric route representations for reservations, enabling route visualization and spatial analysis.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class ReservationPolyline extends Model {
  static get tableName() {
    return 'reservation_polyline';
  }
}
module.exports = ReservationPolyline.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `reservation_polyline`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Reservation route visualization
- Geometric route storage
- Spatial analysis support
- Route planning optimization

## Polyline Features
- **Route Geometry**: Complete path representation
- **Waypoint Storage**: Intermediate stops
- **Distance Calculations**: Route length metrics
- **Complexity Handling**: Multi-segment routes

## Key Features
- Compressed polyline encoding
- Efficient spatial storage
- Route visualization support
- Geographic analysis capabilities

## Geometric Data
- **Encoded Polylines**: Compressed route representation
- **Coordinate Sequences**: GPS point series
- **Elevation Data**: Height profile information
- **Route Metadata**: Distance, duration, complexity

## Integration Points
- **Reservations**: Route planning for bookings
- **TripTrajectory**: Actual vs planned routes
- **ActivityArea**: Route-area relationships
- **CmLocation**: Location-based routing

## Spatial Applications
- Route visualization in maps
- Distance and duration calculations
- Geographic analysis and reporting
- Route optimization algorithms

## Performance Features
- Compressed polyline storage
- Efficient spatial queries
- Fast route rendering
- Optimized for mapping applications

## Visualization Support
- Map rendering compatibility
- Route display optimization
- Interactive route exploration
- Multi-platform visualization

## Related Models
- Reservations: Route planning
- TripTrajectory: Actual routes
- ActivityArea: Spatial regions
- CmLocation: Location targeting

## Development Notes
- Spatial data optimization critical
- Mapping integration essential
- Compression algorithms important
- Visualization performance key